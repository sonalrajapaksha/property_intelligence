import json
import random
from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .db import ImportJob, Property, RawObservation, Source, Transaction
from .pipeline import match_score

REGIONS = [
    ("Auckland", "Auckland", -36.85, 174.76),
    ("Wellington", "Wellington", -41.29, 174.78),
    ("Canterbury", "Christchurch", -43.53, 172.63),
    ("Waikato", "Hamilton", -37.78, 175.28),
    ("Bay of Plenty", "Tauranga", -37.69, 176.17),
    ("Otago", "Dunedin", -45.87, 170.50),
    ("Manawatū-Whanganui", "Palmerston North", -40.35, 175.61),
]
STREETS = [
    "Queen St",
    "Great South Rd",
    "Victoria St",
    "High St",
    "Main Rd",
    "Cameron Rd",
    "Lincoln Rd",
    "George St",
    "Riccarton Rd",
    "Broadway",
]
TENANTS = {
    "SERVICE_STATION": ["BP", "Z Energy", "Mobil", "Gull"],
    "QSR": ["McDonald's", "KFC", "Burger King", "Subway"],
    "HEALTHCARE": ["Healthpoint", "Southern Cross", "Care Clinic", "MedLab"],
}


def seed(session: Session) -> None:
    if session.scalar(select(func.count(Property.id))):
        return
    rng = random.Random(21031926)
    source = Source(
        name="Synthetic demonstration dataset",
        source_type="DEMO",
        reference="Generated with fixed seed 21031926",
    )
    job = ImportJob(
        filename="synthetic_demo.csv",
        records_received=760,
        records_imported=723,
        records_rejected=25,
        records_flagged=12,
        status="COMPLETE",
    )
    session.add_all([source, job])
    session.flush()
    properties = []
    for i in range(420):
        region, city, lat, lon = REGIONS[i % len(REGIONS)]
        sector = list(TENANTS)[i % 3]
        number = 12 + i * 3
        address = f"{number} {STREETS[i % len(STREETS)]}, {city}"
        land = round(rng.uniform(450, 4500), 1)
        property = Property(
            canonical_address=address,
            street_address=address.split(",")[0],
            city=city,
            region=region,
            postcode=str(1000 + i % 8000),
            latitude=lat + rng.uniform(-0.12, 0.12),
            longitude=lon + rng.uniform(-0.12, 0.12),
            sector=sector,
            land_area_m2=land,
            building_area_m2=round(land * rng.uniform(0.12, 0.8), 1),
            owner_name=None if i % 19 == 0 else f"{city} Property Holdings Ltd",
            tenant_name=None if i >= 12 and i % 23 == 0 else rng.choice(TENANTS[sector]),
        )
        properties.append(property)
    session.add_all(properties)
    session.flush()
    today = date.today()
    for i in range(610):
        p = properties[i % len(properties)]
        years_ago = rng.randrange(0, 8)
        day = today - timedelta(days=years_ago * 365 + rng.randrange(0, 350))
        price = round(rng.lognormvariate(15.0, 0.55) / 10000) * 10000
        session.add(
            Transaction(
                property_id=p.id,
                transaction_date=day,
                sale_price=price,
                buyer_name=f"Buyer {i % 48} Ltd",
                seller_name=f"Seller {i % 36} Ltd",
                reported_yield=round(rng.uniform(0.035, 0.09), 4) if i % 9 else None,
                land_area_m2=p.land_area_m2,
                building_area_m2=p.building_area_m2,
                source_id=source.id,
            )
        )
    for i in range(760):
        p = properties[i % len(properties)]
        address = (
            p.canonical_address.replace(" St", " Street")
            if i % 3 == 0
            else p.canonical_address.upper()
            if i % 3 == 1
            else p.canonical_address
        )
        raw_price = "$4.2m" if i % 5 == 0 else "4,200,000" if i % 5 == 1 else "$4200000"
        land_area = p.land_area_m2 or 0
        area = f"{land_area:,.0f} sqm" if i % 2 else f"{land_area / 10000:.4f} ha"
        status = "REVIEW" if i < 12 else "REJECTED" if i < 37 else "IMPORTED"
        raw_tenant = "Alternative Operator" if status == "REVIEW" else p.tenant_name
        score, _ = match_score(
            {"address": address, "city": p.city, "land_area_m2": land_area, "tenant": raw_tenant}, p
        )
        payload = {
            "Property Address": address,
            "City": p.city,
            "Tenant": raw_tenant,
            "Site Area": area,
            "Sale Amount": raw_price,
            "Settlement Date": "14 Mar 2026",
        }
        session.add(
            RawObservation(
                import_job_id=job.id,
                raw_address=address,
                raw_owner=p.owner_name,
                raw_tenant=raw_tenant,
                raw_sale_price="-2" if status == "REJECTED" else raw_price,
                raw_sale_date="03/04/2026" if status == "REJECTED" else "14 Mar 2026",
                raw_land_area=area,
                raw_payload_json=json.dumps(payload),
                status=status,
                matched_property_id=p.id if status == "REVIEW" else None,
                match_score=score if status == "REVIEW" else None,
                issues_json=json.dumps(
                    [
                        {
                            "severity": "error",
                            "field": "sale_price",
                            "rule": "positive",
                            "message": "Sale price must be greater than zero.",
                        }
                    ]
                    if status == "REJECTED"
                    else []
                ),
            )
        )
    job.completed_at = source.retrieved_at
    session.commit()
