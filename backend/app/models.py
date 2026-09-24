import builtins
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Index, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def now() -> datetime:
    return datetime.now(timezone.utc)


class Property(Base):
    __tablename__ = "properties"
    id: Mapped[int] = mapped_column(primary_key=True)
    canonical_address: Mapped[str] = mapped_column(String(300), index=True)
    street_address: Mapped[str | None] = mapped_column(String(200))
    suburb: Mapped[str | None] = mapped_column(String(120))
    city: Mapped[str | None] = mapped_column(String(120), index=True)
    region: Mapped[str | None] = mapped_column(String(120), index=True)
    postcode: Mapped[str | None] = mapped_column(String(4))
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    sector: Mapped[str] = mapped_column(String(24), index=True)
    land_area_m2: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    building_area_m2: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    owner_name: Mapped[str | None] = mapped_column(String(200))
    tenant_name: Mapped[str | None] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="property")

    __table_args__ = (CheckConstraint("sector IN ('SERVICE_STATION','QSR','HEALTHCARE','OTHER')", name="property_sector"),)


class Source(Base):
    __tablename__ = "sources"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    source_type: Mapped[str] = mapped_column(String(40))
    reference: Mapped[str | None] = mapped_column(Text)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="source")


class ImportJob(Base):
    __tablename__ = "import_jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    records_received: Mapped[int] = mapped_column(default=0)
    records_imported: Mapped[int] = mapped_column(default=0)
    records_rejected: Mapped[int] = mapped_column(default=0)
    records_flagged: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(24), default="PENDING")
    observations: Mapped[list["RawObservation"]] = relationship(back_populates="import_job")


class RawObservation(Base):
    __tablename__ = "raw_observations"
    id: Mapped[int] = mapped_column(primary_key=True)
    import_job_id: Mapped[int] = mapped_column(ForeignKey("import_jobs.id"), index=True)
    raw_payload: Mapped[dict] = mapped_column(JSON)
    raw_address: Mapped[str | None] = mapped_column(Text)
    raw_owner: Mapped[str | None] = mapped_column(Text)
    raw_tenant: Mapped[str | None] = mapped_column(Text)
    raw_sale_price: Mapped[str | None] = mapped_column(Text)
    raw_sale_date: Mapped[str | None] = mapped_column(Text)
    raw_land_area: Mapped[str | None] = mapped_column(Text)
    raw_building_area: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(24), default="PENDING", index=True)
    issues: Mapped[list] = mapped_column(JSON, default=list)
    normalized_payload: Mapped[dict | None] = mapped_column(JSON)
    candidate_property_id: Mapped[int | None] = mapped_column(ForeignKey("properties.id"))
    match_score: Mapped[float | None]
    match_evidence: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    import_job: Mapped[ImportJob] = relationship(back_populates="observations")


class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"), index=True)
    transaction_date: Mapped[date] = mapped_column(Date, index=True)
    sale_price: Mapped[Decimal] = mapped_column(Numeric(16, 2))
    buyer_name: Mapped[str | None] = mapped_column(String(200))
    seller_name: Mapped[str | None] = mapped_column(String(200))
    reported_yield: Mapped[Decimal | None] = mapped_column(Numeric(7, 5))
    land_area_m2: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    building_area_m2: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    property: Mapped[Property] = relationship(back_populates="transactions")
    source: Mapped[Source | None] = relationship(back_populates="transactions")

    __table_args__ = (Index("ix_transaction_property_date", "property_id", "transaction_date"),)

    @builtins.property
    def price_per_land_m2(self) -> Decimal | None:
        return self.sale_price / self.land_area_m2 if self.land_area_m2 and self.land_area_m2 > 0 else None

    @builtins.property
    def price_per_building_m2(self) -> Decimal | None:
        return self.sale_price / self.building_area_m2 if self.building_area_m2 and self.building_area_m2 > 0 else None
