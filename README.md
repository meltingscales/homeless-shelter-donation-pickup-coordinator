# Shelter Pickup Coordinator

A platform for coordinating donation pickups between donors and homeless shelters.

## Overview

This application helps coordinate picking up donated goods by connecting donors with shelters:
- Donors can publish items they wish to donate and their location
- Shelters can display needed items and plan pickup routes
- Route optimization helps shelters efficiently collect donations

## Features

- **Geospatial search** - Find donations or shelters near a location
- **Structured item categories** - Food, clothing, toiletries, bedding, and more
- **Route planning** - Shelters can plan and optimize pickup routes
- **JWT authentication** - Secure user accounts with role-based access
- **Item matching** - Shelters can find donations matching their needs

## Quick Start

```bash
# Install dependencies (Python 3.11+)
pip install -e .

# Run with SQLite (development)
export USE_POSTGIS=false
uvicorn main:app --reload

# Or with PostgreSQL + PostGIS
export USE_POSTGIS=true
export DATABASE_URL="postgresql://user:pass@localhost:5432/shelter"
export SECRET_KEY="your-secret-key"
uvicorn main:app --reload
```

## Environment Variables

See `.env.example` for required environment variables:

```bash
# Database
USE_POSTGIS=true                    # Set false for SQLite
DATABASE_URL=postgresql://...       # Postgres connection string

# Authentication
SECRET_KEY=your-secret-key-here     # Generate with: openssl rand -hex 32

# Optional
GOOGLE_MAPS_API_KEY=your-key        # For address geocoding
```

## API Documentation

When running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

See [API.md](API.md) for detailed endpoint documentation.

## Project Structure

```
app/
├── api/           # API endpoints (auth, donations, shelters, routes, items)
├── core/          # Database, auth, config, geocoding, items utilities
├── models/        # SQLAlchemy models (User, Donation, Shelter, Route, Pickup)
└── schemas/       # Pydantic schemas for request/response validation
tests/             # Pytest tests
main.py            # FastAPI application entry point
pyproject.toml     # Project dependencies
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest httpx pytest-asyncio

# Run tests
pytest

# Run with coverage
pip install pytest-cov
pytest --cov=app --cov-report=html
```

### Database Setup

**PostgreSQL + PostGIS (Recommended):**
```bash
# Create database
createdb shelter_pickup
psql shelter_pickup -c "CREATE EXTENSION postgis;"

# Run migrations (if using Alembic in future)
# alembic upgrade head
```

**SQLite (Development):**
```bash
# Just run the app - tables are created automatically
export USE_POSTGIS=false
uvicorn main:app --reload
```

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy 2.0** - ORM for database operations
- **Pydantic** - Data validation
- **PostgreSQL + PostGIS** - Geospatial database (optional)
- **GeoAlchemy2** - PostGIS integration
- **JWT** - Authentication via python-jose
- **Pytest** - Testing framework

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the migration progress from Django to FastAPI.

**Current Progress: 65%**
- ✅ Phase 1: Foundation
- ✅ Phase 2: Database & Geospatial
- ✅ Phase 3: Authentication & Users
- ✅ Phase 4: Item Categories & Route Planning
- 🔄 Phase 5: Frontend & Deployment (in progress)
- 🔄 Phase 6: Testing & Documentation (in progress)

## License

See [LISCENSE](LISCENSE) file.

---

## Legacy Django Information

The original Django application has been archived to `old-code/`. See the old documentation below for reference.

### Old App (Heroku)

The legacy Django app was available at: https://shelter-pickup-coordinator.herokuapp.com/

### Legacy Documentation

**For donaters:**
- List what items they wish to donate
- Publish their location to homeless shelters to optimize collection routes
- See which shelters, where, need what items
- Get notified of pickup routes

**For shelters:**
- Publicly display needed items
- See all people who have things to donate
- Plan routes based on customizable criteria:
  - Distance, needed items
  - Statistics: best geo-locations for most items, item-yield of routes, heatmap of item density
  - By item group: Clothing (winter/summer), Food (canned/produce)

### Legacy Dependencies

The old Django code required:
- Python >= 3.6
- pipenv (see `old-code/Pipfile`)
- PostgreSQL with PostGIS
- Geospatial libraries: GEOS, GDAL, PROJ.4

### Contact

For questions about the legacy code, contact the original maintainer.
