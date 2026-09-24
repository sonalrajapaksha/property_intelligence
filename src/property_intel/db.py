import builtins
from datetime import date, datetime
from pathlib import Path

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from .config import DB_PATH


class Base(DeclarativeBase):
    pass


class Property(Base):
    __tablename__ = "properties"
    id: Mapped[int] = mapped_column(primary_key=True)
    canonical_address: Mapped[str] = mapped_column(String(300), index=True)
    street_address: Mapped[str | None] = mapped_column(String(200))
    suburb: Mapped[str | None] = mapped_column(String(100))
    city: Mapped[str | None] = mapped_column(String(100))
    region: Mapped[str | None] = mapped_column(String(100), index=True)
    postcode: Mapped[str | None] = mapped_column(String(4))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    sector: Mapped[str] = mapped_column(String(32), index=True, default="OTHER")
    land_area_m2: Mapped[float | None] = mapped_column(Float)
    building_area_m2: Mapped[float | None] = mapped_column(Float)
    owner_name: Mapped[str | None] = mapped_column(String(200))
    tenant_name: Mapped[str | None] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="property")


class Source(Base):
    __tablename__ = "sources"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    source_type: Mapped[str] = mapped_column(String(40))
    reference: Mapped[str | None] = mapped_column(String(300))
    retrieved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"), index=True)
    transaction_date: Mapped[date] = mapped_column(Date, index=True)
    sale_price: Mapped[float] = mapped_column(Float)
    buyer_name: Mapped[str | None] = mapped_column(String(200))
    seller_name: Mapped[str | None] = mapped_column(String(200))
    reported_yield: Mapped[float | None] = mapped_column(Float)
    land_area_m2: Mapped[float | None] = mapped_column(Float)
    building_area_m2: Mapped[float | None] = mapped_column(Float)
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    property: Mapped[Property] = relationship(back_populates="transactions")
    source: Mapped[Source | None] = relationship()

    @builtins.property
    def price_per_land_m2(self) -> float | None:
        return self.sale_price / self.land_area_m2 if self.land_area_m2 else None

    @builtins.property
    def price_per_building_m2(self) -> float | None:
        return self.sale_price / self.building_area_m2 if self.building_area_m2 else None


class ImportJob(Base):
    __tablename__ = "import_jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(300))
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    records_received: Mapped[int] = mapped_column(Integer, default=0)
    records_imported: Mapped[int] = mapped_column(Integer, default=0)
    records_rejected: Mapped[int] = mapped_column(Integer, default=0)
    records_flagged: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(30), default="RUNNING")


class RawObservation(Base):
    __tablename__ = "raw_observations"
    id: Mapped[int] = mapped_column(primary_key=True)
    import_job_id: Mapped[int] = mapped_column(ForeignKey("import_jobs.id"), index=True)
    raw_address: Mapped[str | None] = mapped_column(String(300))
    raw_owner: Mapped[str | None] = mapped_column(String(200))
    raw_tenant: Mapped[str | None] = mapped_column(String(200))
    raw_sale_price: Mapped[str | None] = mapped_column(String(100))
    raw_sale_date: Mapped[str | None] = mapped_column(String(100))
    raw_land_area: Mapped[str | None] = mapped_column(String(100))
    raw_building_area: Mapped[str | None] = mapped_column(String(100))
    raw_payload_json: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="PENDING")
    matched_property_id: Mapped[int | None] = mapped_column(ForeignKey("properties.id"))
    match_score: Mapped[float | None] = mapped_column(Float)
    issues_json: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


def open_db(path: Path = DB_PATH) -> Session:
    path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{path}")
    Base.metadata.create_all(engine)
    return Session(engine)
