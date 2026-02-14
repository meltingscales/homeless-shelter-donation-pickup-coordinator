"""
Tests for authentication endpoints.
"""
import pytest


class TestAuthRegister:
    """Tests for user registration."""

    def test_register_success(self, client, test_user_data):
        """Test successful user registration."""
        response = client.post("/api/auth/register", json=test_user_data)
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == test_user_data["email"]
        assert data["user"]["name"] == test_user_data["name"]

    def test_register_duplicate_email(self, client, test_user_data):
        """Test registering with duplicate email fails."""
        # First registration
        client.post("/api/auth/register", json=test_user_data)

        # Second registration with same email
        response = client.post("/api/auth/register", json=test_user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_register_weak_password(self, client, test_user_data):
        """Test registration with weak password fails."""
        test_user_data["password"] = "weak"
        response = client.post("/api/auth/register", json=test_user_data)
        assert response.status_code == 422  # Validation error

    def test_register_shelter_staff_without_shelter(self, client, test_user_data):
        """Test shelter_staff registration without shelter_id fails."""
        test_user_data["role"] = "shelter_staff"
        response = client.post("/api/auth/register", json=test_user_data)
        assert response.status_code == 400
        assert "shelter_id" in response.json()["detail"].lower()


class TestAuthLogin:
    """Tests for user login."""

    def test_login_success(self, client, test_user_data):
        """Test successful login."""
        # Register first
        client.post("/api/auth/register", json=test_user_data)

        # Login
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == test_user_data["email"]

    def test_login_wrong_email(self, client, test_user_data):
        """Test login with wrong email fails."""
        login_data = {
            "email": "wrong@example.com",
            "password": test_user_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401

    def test_login_wrong_password(self, client, test_user_data):
        """Test login with wrong password fails."""
        # Register first
        client.post("/api/auth/register", json=test_user_data)

        # Login with wrong password
        login_data = {
            "email": test_user_data["email"],
            "password": "WrongPassword123!"
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401


class TestAuthMe:
    """Tests for getting current user."""

    def test_get_me_success(self, client, auth_headers):
        """Test getting current user profile."""
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert "email" in data
        assert "name" in data
        assert "role" in data

    def test_get_me_no_token(self, client):
        """Test getting profile without auth token fails."""
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_get_me_invalid_token(self, client):
        """Test getting profile with invalid token fails."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 401


class TestAuthLogout:
    """Tests for logout."""

    def test_logout(self, client, auth_headers):
        """Test logout endpoint."""
        response = client.post("/api/auth/logout", headers=auth_headers)
        assert response.status_code == 200
        assert "successfully" in response.json()["message"].lower()
