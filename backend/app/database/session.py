import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

logger = logging.getLogger("land_acquisition_db")
Base = declarative_base()

def get_database_engine():
    """
    Attempts to connect to PostgreSQL as configured.
    Falls back gracefully to SQLite local database if PostgreSQL instance is unavailable.
    """
    db_url = settings.DATABASE_URL
    try:
        if db_url.startswith("postgresql"):
            logger.info("Attempting connection to PostgreSQL database at %s", db_url)
            engine = create_engine(db_url, pool_pre_ping=True, pool_size=10, max_overflow=20)
            # Test connection
            with engine.connect() as conn:
                pass
            logger.info("Successfully connected to PostgreSQL.")
            return engine
    except Exception as e:
        logger.warning(
            "Could not connect to PostgreSQL (%s). Falling back to SQLite local database: %s",
            e,
            settings.SQLITE_FALLBACK_URL,
        )

    # SQLite fallback
    sqlite_url = settings.SQLITE_FALLBACK_URL
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
    logger.info("Using SQLite database at %s", sqlite_url)
    return engine

engine = get_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
