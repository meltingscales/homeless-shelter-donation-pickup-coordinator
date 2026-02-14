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

## Phase 2: Database & Geospatial ✅ COMPLETE

### 2.1 PostGIS Integration ✅ COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| Switch from SQLite to PostgreSQL | ✅ | Toggle via `USE_POSTGIS` env var |
| Add PostGIS extension to DB | ✅ | `init_postgis()` on startup |
| Install GeoAlchemy2 dependency | ✅ | Added to pyproject.toml |
| Add `point` column to models | ✅ | Geometry('POINT', srid=4326) |
| Google Maps geocoding integration | ✅ | `app/core/geocoding.py` |

**Commits:** `50339d4`

### 2.2 Geospatial Queries ✅ COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| Distance-based filtering (find donations near shelter) | ✅ | ST_DWithin queries |
| Location search radius endpoints | ✅ | `/nearby` endpoints |
| Map visualization data endpoints | ⚠️ | Data ready, frontend TBD |

**API Endpoints Added:**
```
GET /api/donations/nearby?lat={lat}&lng={lng}&radius_miles={radius}
GET /api/shelters/nearby?lat={lat}&lng={lng}&radius_miles={radius}
```

**Completed Features:**
- GeoAlchemy2 integration with PostGIS
- Spatially-indexed `location` column on Donation and Shelter
- `latitude`/`longitude` cache columns for easy access
- SQLite fallback for local development (`USE_POSTGIS=false`)
- Google Maps geocoding service (needs API key)
- Distance-based queries with radius filtering
- Results ordered by distance

---

## Phase 3: Authentication & Users ✅ COMPLETE

### 3.1 User System ✅ COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| User model (email, password, role) | ✅ | User model with UserRole enum |
| Password hashing (bcrypt/argon2) | ✅ | passlib with bcrypt |
| JWT token authentication | ✅ | python-jose, 1 week expiry |
| Login/logout endpoints | ✅ | /api/auth/register, /api/auth/login |
| Protected route decorators | ✅ | get_current_user, get_current_donor, get_current_shelter_staff, get_current_admin |
| User registration flow | ✅ | Email verification placeholder |

**Commits:** `a6e6ba8`

**Dependencies Added:**
- python-jose[cryptography] for JWT tokens
- passlib[bcrypt] for password hashing
- python-multipart for form data

**User Roles:**
- `donor`: Can create donations, manage their locations
- `shelter_staff`: Can claim donations, manage shelter profile
- `admin`: Full access

### 3.2 Authorization ✅ COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| Role-based access control | ✅ | Dependency injectors for each role |
| Shelter ownership verification | ✅ | shelter_staff can only claim for their shelter |
| Donation ownership verification | ✅ | /api/donations/my-donations endpoint |

**Protected Endpoints:**
- `POST /api/donations` - Requires auth (links donation to user)
- `GET /api/donations/my-donations` - Get current user's donations
- `POST /api/donations/{id}/claim` - Requires shelter_staff role
- `GET /api/auth/me` - Get current user profile

---

## Phase 4: Advanced Features ✅ COMPLETE (Item & Route Planning)

### 4.1 Item Management System ✅ COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| Item categories (clothing, food, toiletries, etc.) | ✅ | 10+ categories matching legacy |
| Structured item storage (JSON) | ✅ | items_structured + items_text fallback |
| Shelter "needed items" matching | ✅ | find_matching_donations() method |
| Item search/filter endpoints | ✅ | GET /api/items/categories, /api/items/flat |

**Commits:** `b862a88`

**Item Categories:**
- Food (produce, non-perishable, perishable, other)
- Clothing (shoes, legwear, winter, underwear)
- Menstrual products, pharmaceuticals, toiletries
- Cleaning supplies, sexual health, bedding, electronics

### 4.2 Route Planning ✅ COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| Route model (driver, date, status) | ✅ | Route with RouteStatus enum |
| Pickup model (route, donation, status) | ✅ | Pickup with PickupStatus enum |
| Route optimization (nearest neighbor) | ✅ | GET /api/routes/shelter/{id}/optimized |
| Route CRUD endpoints | ✅ | Full CRUD with status updates |
| Add donations to route | ✅ | POST /api/routes/{id}/pickups |
| Mark pickups complete | ✅ | PUT /api/routes/pickups/{id}, skip endpoint |

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

## Phase 6: Testing & Documentation ✅ COMPLETE

### 6.1 Testing ✅ COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| Pytest setup | ✅ | pytest.ini, conftest.py with fixtures |
| API endpoint tests | ✅ | test_auth.py, test_donations.py, test_shelters.py |
| Test fixtures | ✅ | client, db_session, auth_headers, test data |
| Tests README | ✅ | Running instructions in tests/README.md |

**Commits:** `45c3e07`

**Test Coverage:**
- Auth: register, login, get_me, logout (15+ tests)
- Donations: create, list, my-donations, get, claim (10+ tests)
- Shelters: create, list, get, nearby (5+ tests)

### 6.2 Documentation ✅ COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| API documentation | ✅ | API.md with all endpoints |
| Setup/development guide | ✅ | README.md quick start |
| Migration notes | ✅ | ROADMAP.md, README legacy section |
| Auto-generated docs | ✅ | FastAPI Swagger UI at /docs |

**Documentation Files:**
- `API.md` - Complete API endpoint reference
- `README.md` - Updated with FastAPI info, quick start, env vars
- `ROADMAP.md` - Migration progress tracking
- `tests/README.md` - Test running instructions

---

## Legacy Feature Comparison

| Feature | Old Django | New FastAPI | Status |
|---------|------------|-------------|--------|
| User authentication | Django Auth | ✅ JWT + bcrypt | Complete |
| Geospatial queries | PostGIS GeoDjango | ✅ GeoAlchemy2 | Complete |
| Google Maps API | Integrated | ✅ Geocoding service | Complete |
| Route planning | Route + Pickup models | ✅ Route + Pickup models | Complete |
| Item categories | JSONField system | ✅ JSON + categories | Complete |
| Multiple locations per user | Home model | ❌ Missing | Maybe later |
| Profile images | ImageField | ❌ Missing | Maybe later |
| Markdown descriptions | markdown library | ❌ Missing | Maybe later |

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
geoalchemy2>=0.14.0       ✅ PostGIS support
psycopg2-binary>=2.9.0    ✅ PostgreSQL
requests>=2.31.0          ✅ Google Maps API
python-jose[cryptography] ✅ JWT auth
passlib[bcrypt]>=1.7.4    ✅ Password hashing
python-multipart>=0.0.9   ✅ Form data
```

### Still Needed (Future)
```
# Frontend frameworks if needed
# Additional testing tools as coverage grows
```

---

## Progress Tracker

```
Phase 1: Foundation         [████████████████████] 100% COMPLETE
Phase 2: Database/Geospatial [████████████████████] 100% COMPLETE
Phase 3: Auth/Users         [████████████████████] 100% COMPLETE
Phase 4: Advanced Features  [████████████████████] 100% COMPLETE
Phase 5: Frontend/Deploy    [░░░░░░░░░░░░░░░░░░░░]   0% TODO
Phase 6: Testing/Docs       [████████████████████] 100% COMPLETE

Overall Progress:            [█████████████████████]  83%
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
