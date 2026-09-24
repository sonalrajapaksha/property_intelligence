import csv
import json
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from rapidfuzz.fuzz import ratio
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import AUTO_MATCH, MATCH_WEIGHTS, REVIEW_MATCH
from .db import ImportJob, Property, RawObservation, Source, Transaction


def normalise_address(value: str | None) -> str:
    value = re.sub(r"[^\w\s]", " ", (value or "").lower())
    words = {"street": "st", "road": "rd", "avenue": "ave", "mount": "mt", "highway": "hwy"}
    return " ".join(words.get(word, word) for word in value.split())


def normalise_company(value: str | None) -> str:
    value = re.sub(r"[^\w\s]", " ", (value or "").lower())
    return " ".join("ltd" if word == "limited" else word for word in value.split())


def parse_money(value: Any) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    text = str(value).lower().replace(",", "").replace("$", "").strip()
    match = re.fullmatch(r"([+-]?\d+(?:\.\d+)?)\s*(m|million|k|thousand)?", text)
    if not match:
        raise ValueError(f"Invalid currency: {value}")
    return (
        float(match[1]) * {None: 1, "m": 1e6, "million": 1e6, "k": 1e3, "thousand": 1e3}[match[2]]
    )


def parse_area(value: Any) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    text = str(value).lower().replace(",", "").replace("²", "2").strip()
    match = re.fullmatch(r"([+-]?\d+(?:\.\d+)?)\s*(sqm|m2|ha)?", text)
    if not match:
        raise ValueError(f"Invalid area: {value}")
    return float(match[1]) * (10000 if match[2] == "ha" else 1)


def parse_date(value: Any) -> date | None:
    if value is None or str(value).strip() == "":
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value).strip()
    if re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}", text):
        a, b, _ = map(int, text.split("/"))
        if a <= 12 and b <= 12:
            raise ValueError(f"Ambiguous date: {value}; use YYYY-MM-DD")
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d %b %Y", "%d %B %Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Invalid date: {value}")


@dataclass
class Issue:
    severity: str
    field: str
    rule: str
    message: str


def validate(row: dict[str, Any]) -> list[Issue]:
    issues = []

    def add(severity: str, field: str, rule: str, message: str) -> None:
        issues.append(Issue(severity, field, rule, message))

    price = row.get("sale_price")
    if price is not None and price <= 0:
        add("error", "sale_price", "positive", "Sale price must be greater than zero.")
    if price and price > 100_000_000:
        add("warning", "sale_price", "high", "Sale price is unusually high; review the source.")
    if price and price < 100_000:
        add("warning", "sale_price", "low", "Sale price is unusually low; review the source.")
    for key, label in (("land_area_m2", "Land area"), ("building_area_m2", "Building area")):
        if row.get(key) is not None and row[key] <= 0:
            add("error", key, "positive", f"{label} must be greater than zero.")
    if row.get("transaction_date") and row["transaction_date"] > date.today():
        add("error", "transaction_date", "future", "Transaction date is in the future.")
    y = row.get("reported_yield")
    if y is not None and (y < 0 or y > 1):
        add("error", "reported_yield", "range", "Reported yield must be between 0% and 100%.")
    elif y is not None and y > 0.20:
        add("warning", "reported_yield", "high", f"Reported yield of {y:.1%} is unusually high.")
    land, building = row.get("land_area_m2"), row.get("building_area_m2")
    if land and building and building > land * 2:
        add(
            "warning",
            "building_area_m2",
            "large",
            "Building area is more than twice the land area.",
        )
    if price and land and price / land > 100_000:
        add("warning", "sale_price", "unit_price", "Price per land m² is unusually high.")
    for key, label in (("owner", "Owner"), ("tenant", "Tenant")):
        if not row.get(key):
            add("warning", key, "missing", f"{label} is unavailable.")
    return issues


def _unit(address: str) -> str | None:
    match = re.search(r"\bunit\s+(\w+)\b", address)
    return match[1] if match else None


def _number(address: str) -> str | None:
    match = re.search(r"\b(\d+)\b", re.sub(r"\bunit\s+\w+", "", address))
    return match[1] if match else None


def match_score(row: dict[str, Any], property: Property) -> tuple[float, dict[str, float]]:
    a, b = normalise_address(row.get("address")), normalise_address(property.canonical_address)
    if not a or not b or (_number(a) and _number(b) and _number(a) != _number(b)):
        return 0.0, {"address": 0.0}
    if _unit(a) != _unit(b):
        return 0.0, {"unit": 0.0}
    if row.get("postcode") and property.postcode and str(row["postcode"]) != property.postcode:
        return 0.0, {"postcode": 0.0}
    scores = {"address": ratio(a, b) / 100}
    locality = row.get("city") or row.get("region")
    existing = property.city if row.get("city") else property.region
    if locality and existing:
        scores["geography"] = 1.0 if str(locality).lower() == existing.lower() else 0.0
    for key, field in (("land", "land_area_m2"), ("building", "building_area_m2")):
        x, y = row.get(field), getattr(property, field)
        if x and y:
            scores[key] = min(x, y) / max(x, y)
    if row.get("tenant") and property.tenant_name:
        scores["tenant"] = (
            ratio(normalise_company(row["tenant"]), normalise_company(property.tenant_name)) / 100
        )
    weight = sum(MATCH_WEIGHTS[key] for key in scores)
    return sum(
        MATCH_WEIGHTS[key] * score for key, score in scores.items() if key in MATCH_WEIGHTS
    ) / weight, scores


def best_match(
    session: Session, row: dict[str, Any]
) -> tuple[Property | None, float, dict[str, float]]:
    number = _number(normalise_address(row.get("address")))
    candidates = (
        session.scalars(
            select(Property).where(Property.canonical_address.ilike(f"%{number}%"))
        ).all()
        if number
        else []
    )
    ranked = sorted(
        ((match_score(row, p), p) for p in candidates), key=lambda item: item[0][0], reverse=True
    )
    return (ranked[0][1], *ranked[0][0]) if ranked else (None, 0.0, {})


FIELDS = (
    "address",
    "city",
    "region",
    "postcode",
    "sector",
    "owner",
    "tenant",
    "transaction_date",
    "sale_price",
    "land_area_m2",
    "building_area_m2",
    "buyer",
    "seller",
    "reported_yield",
)
ALIASES = {
    "property address": "address",
    "settlement date": "transaction_date",
    "sale amount": "sale_price",
    "site area": "land_area_m2",
    "purchaser": "buyer",
    "vendor": "seller",
    "land area": "land_area_m2",
    "building area": "building_area_m2",
    "yield": "reported_yield",
}


def suggest_mapping(headers: list[str]) -> dict[str, str]:
    return {
        h: ALIASES.get(h.lower().strip(), h.lower().strip().replace(" ", "_"))
        for h in headers
        if ALIASES.get(h.lower().strip(), h.lower().strip().replace(" ", "_")) in FIELDS
    }


def read_rows(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as file:
            return list(csv.DictReader(file))
    if path.suffix.lower() == ".xlsx":
        workbook = load_workbook(path, read_only=True, data_only=True)
        sheet = workbook.active
        if sheet is None:
            raise ValueError("Workbook has no readable worksheet")
        rows = sheet.values
        headers = [str(value or "") for value in next(rows)]
        result = [
            dict(zip(headers, row)) for row in rows if any(value is not None for value in row)
        ]
        workbook.close()
        return result
    raise ValueError("Choose a CSV or XLSX file")


def clean_row(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["sale_price"] = parse_money(row.get("sale_price"))
    for key in ("land_area_m2", "building_area_m2"):
        result[key] = parse_area(row.get(key))
    result["transaction_date"] = parse_date(row.get("transaction_date"))
    y = row.get("reported_yield")
    result["reported_yield"] = (
        float(str(y).replace("%", ""))
        / (100 if "%" in str(y) or (y is not None and float(y) > 1) else 1)
        if y not in (None, "")
        else None
    )
    return result


def import_rows(
    session: Session, rows: list[dict[str, Any]], mapping: dict[str, str], filename: str
) -> ImportJob:
    job = ImportJob(filename=filename, records_received=len(rows))
    session.add(job)
    session.flush()
    source = Source(name=filename, source_type="IMPORT", reference=filename)
    session.add(source)
    session.flush()
    for original in rows:
        row = {field: original.get(column) for column, field in mapping.items()}
        raw = RawObservation(
            import_job_id=job.id,
            raw_address=str(row.get("address") or ""),
            raw_owner=str(row.get("owner") or ""),
            raw_tenant=str(row.get("tenant") or ""),
            raw_sale_price=str(row.get("sale_price") or ""),
            raw_sale_date=str(row.get("transaction_date") or ""),
            raw_land_area=str(row.get("land_area_m2") or ""),
            raw_building_area=str(row.get("building_area_m2") or ""),
            raw_payload_json=json.dumps(original, default=str),
        )
        session.add(raw)
        try:
            cleaned = clean_row(row)
            issues = validate(cleaned)
            if not cleaned.get("address"):
                issues.append(
                    Issue("error", "address", "required", "Property address is required.")
                )
            if any(issue.severity == "error" for issue in issues):
                raw.status = "REJECTED"
                job.records_rejected += 1
            else:
                matched, score, signals = best_match(session, cleaned)
                raw.match_score = score
                if matched and REVIEW_MATCH <= score < AUTO_MATCH:
                    raw.status = "REVIEW"
                    raw.matched_property_id = matched.id
                    job.records_flagged += 1
                else:
                    if not matched or score < AUTO_MATCH:
                        matched = Property(
                            canonical_address=str(cleaned["address"]),
                            street_address=str(cleaned["address"]),
                            city=cleaned.get("city"),
                            region=cleaned.get("region"),
                            postcode=str(cleaned["postcode"]) if cleaned.get("postcode") else None,
                            sector=cleaned.get("sector") or "OTHER",
                            land_area_m2=cleaned.get("land_area_m2"),
                            building_area_m2=cleaned.get("building_area_m2"),
                            owner_name=cleaned.get("owner"),
                            tenant_name=cleaned.get("tenant"),
                        )
                        session.add(matched)
                        session.flush()
                    raw.matched_property_id = matched.id
                    raw.status = "IMPORTED"
                    if cleaned.get("sale_price") and cleaned.get("transaction_date"):
                        session.add(
                            Transaction(
                                property_id=matched.id,
                                transaction_date=cleaned["transaction_date"],
                                sale_price=cleaned["sale_price"],
                                buyer_name=cleaned.get("buyer"),
                                seller_name=cleaned.get("seller"),
                                reported_yield=cleaned.get("reported_yield"),
                                land_area_m2=cleaned.get("land_area_m2"),
                                building_area_m2=cleaned.get("building_area_m2"),
                                source_id=source.id,
                            )
                        )
                    job.records_imported += 1
            raw.issues_json = json.dumps(
                [asdict(issue) for issue in issues]
                + (
                    [
                        {
                            "severity": "info",
                            "field": "match",
                            "rule": "candidate",
                            "message": f"Candidate match {score:.0%}: {signals}",
                        }
                    ]
                    if raw.status == "REVIEW"
                    else []
                )
            )
        except (ValueError, TypeError) as exc:
            raw.status = "REJECTED"
            raw.issues_json = json.dumps([asdict(Issue("error", "row", "parse", str(exc)))])
            job.records_rejected += 1
    job.completed_at = datetime.now()
    job.status = "COMPLETE"
    session.commit()
    return job


def resolve(session: Session, observation: RawObservation, merge: bool) -> None:
    if observation.status != "REVIEW":
        return
    payload = json.loads(observation.raw_payload_json)
    row = clean_row(
        {field: payload.get(column) for column, field in suggest_mapping(list(payload)).items()}
    )
    if merge:
        observation.status = "MERGED"
    else:
        property = Property(
            canonical_address=str(row.get("address") or observation.raw_address),
            street_address=str(row.get("address") or observation.raw_address),
            city=row.get("city"),
            region=row.get("region"),
            sector=row.get("sector") or "OTHER",
        )
        session.add(property)
        session.flush()
        observation.matched_property_id = property.id
        observation.status = "SEPARATE"
    job = session.get(ImportJob, observation.import_job_id)
    source = session.scalar(select(Source).where(Source.name == job.filename)) if job else None
    if row.get("sale_price") and row.get("transaction_date") and observation.matched_property_id:
        session.add(
            Transaction(
                property_id=observation.matched_property_id,
                transaction_date=row["transaction_date"],
                sale_price=row["sale_price"],
                buyer_name=row.get("buyer"),
                seller_name=row.get("seller"),
                reported_yield=row.get("reported_yield"),
                source_id=source.id if source else None,
                land_area_m2=row.get("land_area_m2"),
                building_area_m2=row.get("building_area_m2"),
            )
        )
    session.commit()
