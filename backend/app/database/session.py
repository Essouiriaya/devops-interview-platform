from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

_DB_AVAILABLE = False


def init_db():
    from app.models import models  # noqa: F401 (enregistre les tables)

    Base.metadata.create_all(bind=engine)


def set_db_available(value: bool):
    global _DB_AVAILABLE
    _DB_AVAILABLE = value


def is_db_available() -> bool:
    return _DB_AVAILABLE


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_optional():
    """Dependance FastAPI : None si PostgreSQL indisponible (mode démo)."""
    if not _DB_AVAILABLE:
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()