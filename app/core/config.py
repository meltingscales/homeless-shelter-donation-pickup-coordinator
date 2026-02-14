from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Shelter Pickup Coordinator"
    APP_VERSION: str = "0.1.0"

    # Distance in miles for "nearby" searches
    DEFAULT_SEARCH_RADIUS_MILES: int = 25

    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/shelter_pickup"
    # Fallback to SQLite for development
    SQLITE_URL: str = "sqlite:///./shelter.db"

    # Use PostGIS if available (set to false to use SQLite)
    USE_POSTGIS: bool = True

    # Authentication
    SECRET_KEY: str = "change-this-in-production-use-openssl-rand-hex-32"


settings = Settings()
