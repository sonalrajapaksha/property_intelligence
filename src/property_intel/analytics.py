from collections import Counter
from datetime import date
from math import asin, cos, radians, sin, sqrt
from statistics import median

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .db import Property, RawObservation, Transaction


def money(value: float | None) -> str:
    if value is None:
        return "—"
    return (
        f"${value / 1e9:.2f}b"
        if abs(value) >= 1e9
        else f"${value / 1e6:.2f}m"
        if abs(value) >= 1e6
        else f"${value / 1e3:.0f}k"
        if abs(value) >= 1e3
        else f"${value:,.0f}"
    )


def overview(session: Session) -> dict:
    transactions = session.scalars(select(Transaction)).all()
    observations = session.scalars(select(RawObservation)).all()
    yields = [t.reported_yield for t in transactions if t.reported_yield is not None]
    land_units = [t.price_per_land_m2 for t in transactions if t.price_per_land_m2 is not None]
    building_units = [
        t.price_per_building_m2 for t in transactions if t.price_per_building_m2 is not None
    ]
    return {
        "properties": session.scalar(select(func.count(Property.id))) or 0,
        "transactions": len(transactions),
        "value": sum(t.sale_price for t in transactions),
        "median_price": median(t.sale_price for t in transactions) if transactions else None,
        "median_yield": median(yields) if yields else None,
        "median_land_unit": median(land_units) if land_units else None,
        "median_building_unit": median(building_units) if building_units else None,
        "yield_count": len(yields),
        "review": sum(
            o.status == "REVIEW" or bool(o.issues_json and '"warning"' in o.issues_json)
            for o in observations
        ),
        "year_counts": Counter(t.transaction_date.year for t in transactions),
        "sector_counts": Counter(t.property.sector for t in transactions),
    }


def market_breakdown(session: Session, by: str) -> list[dict]:
    if by not in ("quarter", "sector", "region"):
        raise ValueError("Group by quarter, sector or region")
    groups: dict[str, list[Transaction]] = {}
    for sale in session.scalars(select(Transaction)):
        key = (
            f"{sale.transaction_date.year} Q{(sale.transaction_date.month - 1) // 3 + 1}"
            if by == "quarter"
            else getattr(sale.property, by) or "Unknown"
        )
        groups.setdefault(key, []).append(sale)
    result = []
    for key, sales in sorted(groups.items()):
        yields = [sale.reported_yield for sale in sales if sale.reported_yield is not None]
        land_units = [
            sale.price_per_land_m2 for sale in sales if sale.price_per_land_m2 is not None
        ]
        building_units = [
            sale.price_per_building_m2 for sale in sales if sale.price_per_building_m2 is not None
        ]
        result.append(
            {
                "group": key,
                "transactions": len(sales),
                "value": sum(sale.sale_price for sale in sales),
                "median_price": median(sale.sale_price for sale in sales),
                "median_yield": median(yields) if yields else None,
                "yield_count": len(yields),
                "median_land_unit": median(land_units) if land_units else None,
                "median_building_unit": median(building_units) if building_units else None,
            }
        )
    return result


def haversine(a: Property, b: Property) -> float | None:
    if a.latitude is None or a.longitude is None or b.latitude is None or b.longitude is None:
        return None
    lat1, lon1, lat2, lon2 = map(
        radians, (float(a.latitude), float(a.longitude), float(b.latitude), float(b.longitude))
    )
    dlat, dlon = lat2 - lat1, lon2 - lon1
    return 6371 * 2 * asin(sqrt(sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2))


def comparable_score(
    subject: Property, candidate: Property, sale: Transaction
) -> tuple[float, dict]:
    km = haversine(subject, candidate)
    geo = min(
        (km if km is not None else (0 if subject.region == candidate.region else 100)) / 100, 1
    )

    def difference(a: float | None, b: float | None) -> float:
        return abs(a - b) / max(a, b) if a and b else 0.5

    land = difference(subject.land_area_m2, candidate.land_area_m2)
    building = difference(subject.building_area_m2, candidate.building_area_m2)
    age = min((date.today() - sale.transaction_date).days / (365 * 10), 1)
    sector = 0 if subject.sector == candidate.sector else 1
    distance = 0.30 * geo + 0.22 * land + 0.13 * building + 0.15 * age + 0.20 * sector
    return 1 - distance, {
        "distance_km": km,
        "land_difference": land,
        "building_difference": building,
        "age_years": (date.today() - sale.transaction_date).days / 365,
        "same_sector": sector == 0,
    }


def comparables(
    session: Session, subject: Property, limit: int = 5
) -> list[tuple[Transaction, float, dict]]:
    sales = session.scalars(select(Transaction).where(Transaction.property_id != subject.id)).all()
    ranked = [(sale, *comparable_score(subject, sale.property, sale)) for sale in sales]
    return sorted(ranked, key=lambda item: item[1], reverse=True)[:limit]
