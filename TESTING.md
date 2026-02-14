# Testing Guide

Complete guide for testing the Shelter Pickup Coordinator application.

## Table of Contents
- [Quick Test](#quick-test)
- [Automated Tests](#automated-tests)
- [Manual Testing](#manual-testing)
- [API Testing](#api-testing)
- [Docker Testing](#docker-testing)
- [Test Data](#test-data)

---

## Quick Test

Fastest way to verify everything works:

```bash
# 1. Install dependencies
pip install -e pytest httpx pytest-asyncio

# 2. Run automated tests
pytest -q

# 3. Start the app
export USE_POSTGIS=false
uvicorn main:app --reload
```

Then visit http://localhost:8000

---

## Automated Tests

### Running All Tests

```bash
pytest
```

### With Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_auth.py
pytest tests/test_donations.py
pytest tests/test_shelters.py
```

### Run Specific Test

```bash
pytest tests/test_auth.py::TestAuthLogin::test_login_success
```

### With Coverage

```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
# View report: htmlcov/index.html
```

### Test Files Structure

```
tests/
├── conftest.py           # Fixtures (client, db_session, auth_headers)
├── test_auth.py          # Authentication tests (15+ tests)
├── test_donations.py     # Donation endpoint tests (10+ tests)
└── test_shelters.py      # Shelter endpoint tests (5+ tests)
```

### Available Fixtures

```python
def client(db_session):
    """FastAPI test client with database override"""

def test_user_data():
    """Sample user registration data"""

def test_shelter_data():
    """Sample shelter data"""

def test_donation_data():
    """Sample donation data"""

def auth_headers(client):
    """Headers with valid JWT token"""
```

---

## Manual Testing

### 1. Start the Application

```bash
# With SQLite (development)
export USE_POSTGIS=false
uvicorn main:app --reload

# Or with PostgreSQL + PostGIS
export USE_POSTGIS=true
export DATABASE_URL="postgresql://user:pass@localhost:5432/shelter"
export SECRET_KEY="your-secret-key"
uvicorn main:app --reload
```

### 2. Visit the Application

Open your browser to:
- **Main page**: http://localhost:8000
- **API docs**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

### 3. Test Workflow

#### A. Donor Flow

1. **Register as Donor**
   - Go to http://localhost:8000
   - Click "Register"
   - Fill in:
     - Name: `Test Donor`
     - Email: `donor@test.com`
     - Password: `TestPassword123!`
     - Role: `Donor`
   - Click "Register"

2. **Create a Donation**
   - You should be redirected to the home page
   - Click "Donate Items" (or go to `/donor`)
   - Click "+ New Donation"
   - Fill in:
     - Your Name: `Test Donor`
     - Email: `donor@test.com`
     - Address: `123 Main St`
     - City: `Chicago`
     - State: `IL`
     - ZIP: `60601`
     - Items: `5 blankets, 2 winter coats`
   - Click "Create Donation"

3. **View Your Donations**
   - Your donations should appear in the list
   - Check the stats at the top

#### B. Shelter Staff Flow

1. **Register as Shelter Staff**
   - Logout if logged in
   - Go to http://localhost:8000
   - Click "Register"
   - Fill in:
     - Name: `Shelter Staff`
     - Email: `shelter@test.com`
     - Password: `TestPassword123!`
     - Role: `Shelter Staff`
     - Shelter ID: leave empty for now

2. **Register Your Shelter**
   - Click "Shelter Dashboard" or go to `/shelter`
   - Click "+ Register Shelter"
   - Fill in:
     - Name: `Test Shelter`
     - Contact Name: `John Doe`
     - Email: `shelter@test.com`
     - Address: `456 Shelter Ave`
     - City: `Chicago`
     - State: `IL`
     - ZIP: `60602`
     - Needed Items: `blankets, coats, socks`
   - Click "Register Shelter"
   - Note the shelter ID returned

3. **Update Your Account**
   - Logout
   - Re-register as Shelter Staff with the shelter_id

4. **Browse and Claim Donations**
   - Go to `/shelter`
   - Under "Available Donations", click "Search"
   - Click "Claim This Donation" on any donation
   - Check the "Our Claims" tab to see claimed donations

#### C. Route Planning

1. **Create a Route**
   - Go to `/shelter`
   - Click "Routes" tab
   - Fill in:
     - Route Name: `Friday Pickup Route`
     - Description: `North side pickups`
   - Click "Create Route"

---

## API Testing

### Using Swagger UI (Easiest)

1. Go to http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

### Using curl

#### Authentication

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "donor@test.com",
    "password": "TestPassword123!",
    "name": "Test Donor",
    "role": "donor"
  }'

# Login (save the token)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "donor@test.com",
    "password": "TestPassword123!"
  }' | jq -r '.access_token' > token.txt

# Get current user
TOKEN=$(cat token.txt)
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

#### Donations

```bash
TOKEN=$(cat token.txt)

# Create donation
curl -X POST http://localhost:8000/api/donations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "donor_name": "Jane Doe",
    "donor_email": "jane@example.com",
    "address": "123 Main St",
    "city": "Chicago",
    "state": "IL",
    "zip_code": "60601",
    "items_text": "blankets, coats"
  }'

# List all donations
curl http://localhost:8000/api/donations

# Get my donations
curl -X GET http://localhost:8000/api/donations/my-donations \
  -H "Authorization: Bearer $TOKEN"

# Get nearby donations
curl "http://localhost:8000/api/donations/nearby?lat=41.8781&lng=-87.6298&radius_miles=25"
```

#### Shelters

```bash
# Create shelter
curl -X POST http://localhost:8000/api/shelters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Shelter",
    "contact_name": "John Doe",
    "email": "shelter@test.com",
    "address": "456 Shelter Ave",
    "city": "Chicago",
    "state": "IL",
    "zip_code": "60602",
    "needed_items_text": "blankets, coats"
  }'

# List shelters
curl http://localhost:8000/api/shelters

# Get nearby shelters
curl "http://localhost:8000/api/shelters/nearby?lat=41.8781&lng=-87.6298&radius_miles=50"
```

#### Routes

```bash
SHELTER_TOKEN=$(cat shelter_token.txt)

# Create route
curl -X POST http://localhost:8000/api/routes \
  -H "Authorization: Bearer $SHELTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Route",
    "shelter_id": 1,
    "driver_user_id": 2
  }'

# List routes
curl -X GET http://localhost:8000/api/routes \
  -H "Authorization: Bearer $SHELTER_TOKEN"

# Claim donation
curl -X POST http://localhost:8000/api/donations/1/claim \
  -H "Authorization: Bearer $SHELTER_TOKEN"
```

### Using Python

```python
import requests

BASE = "http://localhost:8000"

# Register
response = requests.post(f"{BASE}/api/auth/register", json={
    "email": "test@example.com",
    "password": "TestPassword123!",
    "name": "Test User",
    "role": "donor"
})
token = response.json()["access_token"]

# Create donation
headers = {"Authorization": f"Bearer {token}"}
requests.post(f"{BASE}/api/donations", headers=headers, json={
    "donor_name": "Jane Doe",
    "donor_email": "jane@example.com",
    "address": "123 Main St",
    "city": "Chicago",
    "state": "IL",
    "zip_code": "60601",
    "items_text": "blankets"
})

# List donations
response = requests.get(f"{BASE}/api/donations")
print(response.json())
```

---

## Docker Testing

### With Docker Compose (PostGIS)

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f web

# Run tests inside container
docker-compose exec web pytest

# Shell into container
docker-compose exec web bash

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Environment Variables in Docker

Create a `.env` file for docker-compose:

```bash
SECRET_KEY=your-secret-key-here
USE_POSTGIS=true
DATABASE_URL=postgresql://shelter_user:shelter_pass@db:5432/shelter_pickup
GOOGLE_MAPS_API_KEY=your-key
```

---

## Test Data

### Sample Donor

```
Name: Alice Walker
Email: alice@example.com
Password: Alice123!
Role: Donor

Donation:
- Address: 123 Oak Street, Chicago, IL 60601
- Items: 5 blankets, 3 winter coats, 10 pairs of socks
```

### Sample Shelter

```
Name: Helping Hands Shelter
Contact: Bob Smith
Email: bob@helpinghands.org
Address: 456 Shelter Ave, Chicago, IL 60602
Needed Items: blankets, coats, soup, toiletries
```

### Sample Shelter Staff User

```
Name: Bob Smith
Email: bob@helpinghands.org
Password: Bob123!
Role: shelter_staff
Shelter ID: 1 (after creating shelter)
```

---

## Common Issues

### Port Already in Use

```bash
# Use a different port
uvicorn main:app --port 8001

# Or kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -e .

# Or use virtual environment
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Database Issues

```bash
# Delete SQLite database and start fresh
rm shelter.db
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -e pytest httpx pytest-asyncio
      - run: pytest
```

---

## Performance Testing

### Load Testing with Locust

```bash
pip install locust

# Create locustfile.py:
from locust import HttpUser, task

class ShelterUser(HttpUser):
    @task
    def view_donations(self):
        self.client.get("/api/donations")

    @task
    def get_item_categories(self):
        self.client.get("/api/items/categories")

# Run locust
locust -f locustfile.py --host=http://localhost:8000
```

Visit http://localhost:8089 for the web interface.
