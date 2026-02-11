# Migration Roadmap: Django → FastAPI

**Branch:** `revitalization`
**Started:** February 2025
**Goal:** Modernize the Shelter Pickup Coordinator from legacy Django to FastAPI

---

## Overview

This roadmap tracks the migration from the old Django/GeoDjango codebase (`old-code/`) to a modern FastAPI application.

**Tech Stack Changes:**
- **Old:** Django 2.2 + GeoDjango + PostGIS + Pipenv
- **New:** FastAPI + SQLAlchemy 2 + Pydantic + uv/pyproject.toml

---

## Phase 1: Foundation ✅ COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| Archive legacy code to `old-code/` | ✅ | Commit: `ebe0311` |
| Create FastAPI project structure | ✅ | `app/`, `main.py`, `pyproject.toml` |
| Base models (Donation, Shelter) | ✅ | SQLAlchemy 2.0 with relationships |
| Basic CRUD API endpoints | ✅ | `app/api/donations.py`, `app/api/shelters.py` |
| Pydantic schemas | ✅ | Request/response validation |

**Completed Features:**
- Create/list donations with status filtering
- Create/list shelters
- Claim donations for shelters
- Static file serving and basic HTML pages

---

## Phase 2: Database & Geospatial (CURRENT)

### 2.1 PostGIS Integration 🔨 IN PROGRESS

| Task | Priority | Effort |
|------|----------|--------|
| Switch from SQLite to PostgreSQL | High | 2h |
| Add PostGIS extension to DB | High | 1h |
| Install GeoAlchemy2 dependency | High | 30m |
| Add `point` column to models | High | 2h |
| Google Maps geocoding integration | High | 3h |

**Action Items:**
```bash
# Add to pyproject.toml dependencies:
# - "geoalchemy2>=0.14.0"
# - "psycopg2-binary>=2.9.0"
# - "requests>=2.31.0"  # for Google Maps API
```

**Model Changes Needed:**
```python
from geoalchemy2 import Geometry

class Donation(Base):
    # Add geospatial column
    location = Column(Geometry('POINT', srid=4326))
    # Remove: address, city, state, zip_code as separate columns?
    # Or keep both for geocoding cache

class Shelter(Base):
    location = Column(Geometry('POINT', srid=4326))
```

### 2.2 Geospatial Queries 🔨 TODO

| Task | Priority | Effort |
|------|----------|--------|
| Distance-based filtering (find donations near shelter) | High | 3h |
| Location search radius endpoints | Medium | 2h |
| Map visualization data endpoints | Medium | 3h |

**API Endpoints to Add:**
```
GET /api/donations/near?lat={lat}&lng={lng}&radius_miles={radius}
GET /api/shelters/near?lat={lat}&lng={lng}&radius_miles={radius}
```

---

## Phase 3: Authentication & Users

### 3.1 User System 🔨 TODO

| Task | Priority | Effort |
|------|----------|--------|
| User model (email, password, role) | High | 2h |
| Password hashing (bcrypt/argon2) | High | 1h |
| JWT token authentication | High | 3h |
| Login/logout endpoints | High | 2h |
| Protected route decorators | High | 1h |
| User registration flow | Medium | 2h |

**Dependencies:**
```bash
# - "fastapi-users>=13.0.0"  OR
# - "python-jose[cryptography]>=3.3.0"
# - "passlib[bcrypt]>=1.7.4"
```

**User Roles (from old code):**
- `donor`: Can create donations, manage their locations
- `shelter_staff`: Can claim donations, manage shelter profile
- `admin`: Full access

### 3.2 Authorization 🔨 TODO

| Task | Priority | Effort |
|------|----------|--------|
| Role-based access control | High | 2h |
| Shelter ownership verification | High | 1h |
| Donation ownership verification | High | 1h |

---

## Phase 4: Advanced Features

### 4.1 Item Management System 🔨 TODO

| Task | Priority | Effort |
|------|----------|--------|
| Item categories (clothing, food, toiletries, etc.) | Medium | 3h |
| Structured item storage (JSON → PostgreSQL JSONB) | Medium | 2h |
| Shelter "needed items" matching | Medium | 2h |
| Item search/filter endpoints | Low | 2h |

**Item Categories (from old `libs/ItemList`):**
- Clothing (winter/summer)
- Food (canned/produce)
- Toiletries
- Bedding (blankets, pillows)
- Electronics

### 4.2 Route Planning 🔨 TODO

| Task | Priority | Effort |
|------|----------|--------|
| Route model (driver, date, status) | Medium | 2h |
| Pickup model (route, donation, status) | Medium | 2h |
| Route optimization (nearest neighbor algorithm) | Low | 4h |
| Route CRUD endpoints | Medium | 2h |
| Add donations to route | Medium | 2h |
| Mark pickups complete | Medium | 1h |

**Models Needed:**
```python
class Route(Base):
    shelter_id = Column(Integer, ForeignKey("shelters.id"))
    driver_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)
    status = Column(String)  # planned, in_progress, completed

class Pickup(Base):
    route_id = Column(Integer, ForeignKey("routes.id"))
    donation_id = Column(Integer, ForeignKey("donations.id"))
    sequence_order = Column(Integer)
    status = Column(String)  # pending, completed, skipped
    notes = Column(Text)
```

### 4.3 Notifications 🔨 TODO

| Task | Priority | Effort |
|------|----------|--------|
| Email notifications for claimed donations | Low | 3h |
| Shelter updates when donations nearby | Low | 4h |
| SMS notifications (optional) | Low | 4h |

---

## Phase 5: Frontend & Deployment

### 5.1 Frontend Pages 🔨 TODO

| Task | Priority | Effort |
|------|----------|--------|
| Donor dashboard (list my donations) | High | 4h |
| Shelter dashboard (view nearby donations) | High | 4h |
| Map view with markers | High | 6h |
| Donation creation form | High | 2h |
| Shelter registration form | Medium | 2h |
| Route planning interface | Low | 4h |

### 5.2 Deployment 🔨 TODO

| Task | Priority | Effort |
|------|----------|--------|
| Docker containerization | High | 2h |
| PostGIS in production (Render/Railway/etc) | High | 2h |
| Environment variable configuration | High | 1h |
| CI/CD pipeline | Medium | 2h |
| Domain/SSL setup | Low | 1h |

**Deployment Options:**
- Render (has PostGIS support)
- Railway
- Fly.io
- DigitalOcean App Platform

---

## Phase 6: Testing & Documentation

### 6.1 Testing 🔨 TODO

| Task | Priority | Effort |
|------|----------|--------|
| Pytest setup | High | 1h |
| Model tests | High | 2h |
| API endpoint tests | High | 3h |
| Geospatial query tests | Medium | 2h |
| Integration tests | Medium | 3h |

### 6.2 Documentation 🔨 TODO

| Task | Priority | Effort |
|------|----------|--------|
| API documentation (FastAPI auto-docs) | High | 1h |
| Setup/development guide | High | 2h |
| Migration notes from old code | Medium | 2h |
| Deployment guide | Medium | 1h |

---

## Legacy Feature Comparison

| Feature | Old Django | New FastAPI | Migration Path |
|---------|------------|-------------|----------------|
| User authentication | Django Auth | ⚠️ Not implemented | Add FastAPI-Users or custom JWT |
| Geospatial queries | PostGIS GeoDjango | ⚠️ Not implemented | Add GeoAlchemy2 |
| Google Maps API | Integrated | ❌ Missing | Add geocoding service |
| Route planning | Route + Pickup models | ❌ Missing | Implement in Phase 4 |
| Item categories | JSONField system | ⚠️ Simplified to Text | Re-implement structured items |
| Multiple locations per user | Home model | ❌ Missing | Add later if needed |
| Profile images | ImageField | ❌ Missing | Add file upload handling |
| Markdown descriptions | markdown library | ❌ Missing | Add if needed |

---

## Dependencies Status

### Currently Installed (pyproject.toml)
```
fastapi>=0.115.0          ✅
uvicorn[standard]>=0.32.0 ✅
sqlalchemy>=2.0.0         ✅
pydantic>=2.0.0           ✅
pydantic-settings>=2.0.0  ✅
email-validator>=2.0.0    ✅
```

### Still Needed
```
geoalchemy2>=0.14.0       🔨 PostGIS support
psycopg2-binary>=2.9.0    🔨 PostgreSQL
python-jose[cryptography] 🔨 JWT auth
passlib[bcrypt]>=1.7.4    🔨 Password hashing
requests>=2.31.0          🔨 Google Maps API
pytest>=7.0.0             🔨 Testing
httpx>=0.24.0             🔨 Testing client
```

---

## Progress Tracker

```
Phase 1: Foundation         [████████████████████] 100% COMPLETE
Phase 2: Database/Geospatial [███░░░░░░░░░░░░░░░░]  15% in progress
Phase 3: Auth/Users         [░░░░░░░░░░░░░░░░░░░░]   0% TODO
Phase 4: Advanced Features  [░░░░░░░░░░░░░░░░░░░░]   0% TODO
Phase 5: Frontend/Deploy    [░░░░░░░░░░░░░░░░░░░░]   0% TODO
Phase 6: Testing/Docs       [░░░░░░░░░░░░░░░░░░░░]   0% TODO

Overall Progress:            [███░░░░░░░░░░░░░░░░░]  15%
```

---

## Quick Reference

### Old Code Locations
- Models: `old-code/server/donationcoordinator/{donationcoordinator,org,donator}/models.py`
- Views: `old-code/server/donationcoordinator/{org,donator}/views.py`
- Settings: `old-code/server/donationcoordinator/donationcoordinator/settings.py`
- Item lists: `old-code/server/donationcoordinator/donator/libs.py`

### New Code Locations
- Models: `app/models/{donation,shelter}.py`
- API: `app/api/{donations,shelters}.py`
- Schemas: `app/schemas/{donation,shelter}.py`
- Config: `app/core/{config,database}.py`

---

## Notes

- The old code used **GeoDjango** heavily for location features - this is critical to restore
- **Google Maps API** key was required for geocoding - need to add this back
- Old code had a sophisticated **item categorization system** with JSON structures
- **Route planning** was a key differentiator - should be prioritized after basic features work
- The old code supported **multiple homes per user** - may want to add this back later
