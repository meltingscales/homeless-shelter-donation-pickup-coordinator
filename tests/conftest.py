"""
Test configuration and fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db


# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a test client with a database session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def test_password():
    """Test password."""
    return "TestPassword123!"


@pytest.fixture
def test_user_data():
    """Test user data."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "name": "Test User",
        "phone": "555-1234",
        "role": "donor"
    }


@pytest.fixture
def auth_headers(client, test_user_data):
    """Create a user and return auth headers."""
    # Register user
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_shelter_data():
    """Test shelter data."""
    return {
        "name": "Test Shelter",
        "contact_name": "John Doe",
        "email": "shelter@example.com",
        "phone": "555-9999",
        "address": "123 Shelter St",
        "city": "Chicago",
        "state": "IL",
        "zip_code": "60601",
        "description": "A test shelter",
        "needed_items_text": "blankets, coats"
    }


@pytest.fixture
def test_donation_data():
    """Test donation data."""
    return {
        "donor_name": "Jane Doe",
        "donor_email": "jane@example.com",
        "donor_phone": "555-5678",
        "address": "456 Donation Ave",
        "city": "Chicago",
        "state": "IL",
        "zip_code": "60602",
        "items_text": " blankets, coats, socks",
        "notes": "Please pickup by Friday"
    }
