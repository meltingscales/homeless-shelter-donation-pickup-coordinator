# Tests

This directory contains the test suite for the Shelter Pickup Coordinator API.

## Running Tests

```bash
# Install test dependencies
pip install pytest httpx pytest-asyncio

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::TestAuthLogin::test_login_success

# Run with coverage
pip install pytest-cov
pytest --cov=app --cov-report=html
```

## Test Structure

- `conftest.py` - Fixtures and test configuration
- `test_auth.py` - Authentication endpoint tests
- `test_donations.py` - Donation endpoint tests
- `test_shelters.py` - Shelter endpoint tests

## Fixtures

- `client` - FastAPI test client with database override
- `db_session` - Fresh SQLite database for each test
- `auth_headers` - Headers with valid JWT token
- `test_user_data` - Sample user registration data
- `test_shelter_data` - Sample shelter data
- `test_donation_data` - Sample donation data
