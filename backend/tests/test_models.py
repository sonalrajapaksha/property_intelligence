from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import ImportJob, Property, RawObservation, Source, Transaction


def test_models_keep_raw_and_derive_unit_prices():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        job = ImportJob(filename="demo.csv")
        source = Source(name="Demo", source_type="UPLOAD")
        prop = Property(canonical_address="123 Queen St, Auckland", sector="QSR")
        db.add_all([job, source, prop])
        db.flush()
        raw = RawObservation(import_job_id=job.id, raw_payload={"Address": "123 QUEEN STREET"}, raw_address="123 QUEEN STREET")
        sale = Transaction(property_id=prop.id, transaction_date=date(2024, 5, 1), sale_price=Decimal("4200000"), land_area_m2=Decimal("1000"), source_id=source.id)
        db.add_all([raw, sale])
        db.commit()
        assert sale.price_per_land_m2 == Decimal("4200")
        assert sale.price_per_building_m2 is None
        assert db.get(RawObservation, raw.id).raw_address == "123 QUEEN STREET"
