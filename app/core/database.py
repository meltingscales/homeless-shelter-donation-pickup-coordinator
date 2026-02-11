from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings

# Choose database based on settings
if settings.USE_POSTGIS:
    # PostgreSQL with PostGIS
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
    )
else:
    # Fallback to SQLite for development
    engine = create_engine(
        settings.SQLITE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_postgis():
    """Initialize PostGIS extension on the database."""
    if not settings.USE_POSTGIS:
        return

    with engine.connect() as conn:
        # Enable PostGIS extension
        conn.execute(conn.compile("CREATE EXTENSION IF NOT EXISTS postgis"))
        conn.commit()
