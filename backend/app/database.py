import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://property:property_dev@localhost:5432/property_intelligence")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
