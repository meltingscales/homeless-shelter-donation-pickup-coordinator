"""
Tests for donation endpoints.
"""
import pytest


class TestDonationsCreate:
    """Tests for creating donations."""

    def test_create_donation_authenticated(self, client, auth_headers, test_donation_data):
        """Test creating donation while authenticated."""
        response = client.post("/api/donations", json=test_donation_data, headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert data["donor_name"] == test_donation_data["donor_name"]
        assert data["status"] == "available"
        assert data["zip_code"] == test_donation_data["zip_code"]

    def test_create_donation_unauthenticated(self, client, test_donation_data):
        """Test creating donation without authentication fails."""
        response = client.post("/api/donations", json=test_donation_data)
        assert response.status_code == 401

    def test_create_donation_with_structured_items(self, client, auth_headers, test_donation_data):
        """Test creating donation with structured items."""
        test_donation_data["items_structured"] = {
            "food": {
                "produce": {"lettuce": 5, "apples": 10}
            }
        }
        del test_donation_data["items_text"]

        response = client.post("/api/donations", json=test_donation_data, headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert data["items_structured"]["food"]["produce"]["lettuce"] == 5


class TestDonationsList:
    """Tests for listing donations."""

    def test_list_donations(self, client, auth_headers, test_donation_data):
        """Test listing all donations."""
        # Create a donation
        client.post("/api/donations", json=test_donation_data, headers=auth_headers)

        # List donations
        response = client.get("/api/donations")
        assert response.status_code == 200

        data = response.json()
        assert len(data) >= 1

    def test_list_donations_by_status(self, client, auth_headers, test_donation_data):
        """Test filtering donations by status."""
        # Create a donation
        client.post("/api/donations", json=test_donation_data, headers=auth_headers)

        # Filter by status
        response = client.get("/api/donations?status=available")
        assert response.status_code == 200

        data = response.json()
        assert all(d["status"] == "available" for d in data)

    def test_list_donations_by_zip(self, client, auth_headers, test_donation_data):
        """Test filtering donations by zip code."""
        # Create a donation
        client.post("/api/donations", json=test_donation_data, headers=auth_headers)

        # Filter by zip code
        response = client.get(f"/api/donations?zip_code={test_donation_data['zip_code']}")
        assert response.status_code == 200

        data = response.json()
        assert all(d["zip_code"] == test_donation_data["zip_code"] for d in data)


class TestDonationsMy:
    """Tests for listing user's own donations."""

    def test_my_donations(self, client, auth_headers, test_donation_data):
        """Test getting only my donations."""
        # Create a donation
        client.post("/api/donations", json=test_donation_data, headers=auth_headers)

        # Get my donations
        response = client.get("/api/donations/my-donations", headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert len(data) >= 1

    def test_my_donations_unauthenticated(self, client):
        """Test getting my donations without auth fails."""
        response = client.get("/api/donations/my-donations")
        assert response.status_code == 401


class TestDonationsGet:
    """Tests for getting a specific donation."""

    def test_get_donation(self, client, auth_headers, test_donation_data):
        """Test getting a specific donation."""
        # Create a donation
        create_response = client.post("/api/donations", json=test_donation_data, headers=auth_headers)
        donation_id = create_response.json()["id"]

        # Get the donation
        response = client.get(f"/api/donations/{donation_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == donation_id

    def test_get_donation_not_found(self, client):
        """Test getting non-existent donation."""
        response = client.get("/api/donations/99999")
        assert response.status_code == 404


class TestDonationsClaim:
    """Tests for claiming donations."""

    def test_claim_donation_as_shelter_staff(self, client, test_shelter_data, test_donation_data):
        """Test claiming a donation as shelter staff."""
        # Create a shelter
        client.post("/api/shelters", json=test_shelter_data)

        # Create a shelter staff user
        shelter_user_data = {
            "email": "shelter@example.com",
            "password": "TestPassword123!",
            "name": "Shelter Staff",
            "role": "shelter_staff",
            "shelter_id": 1
        }
        reg_response = client.post("/api/auth/register", json=shelter_user_data)
        shelter_token = reg_response.json()["access_token"]
        shelter_headers = {"Authorization": f"Bearer {shelter_token}"}

        # Create a donation (as donor)
        donor_data = {
            "email": "donor@example.com",
            "password": "TestPassword123!",
            "name": "Donor User",
            "role": "donor"
        }
        client.post("/api/auth/register", json=donor_data)
        donor_login = client.post("/api/auth/login", json={"email": "donor@example.com", "password": "TestPassword123!"})
        donor_token = donor_login.json()["access_token"]
        donor_headers = {"Authorization": f"Bearer {donor_token}"}

        client.post("/api/donations", json=test_donation_data, headers=donor_headers)

        # Claim the donation
        response = client.post("/api/donations/1/claim", headers=shelter_headers)
        assert response.status_code == 200

    def test_claim_donation_as_donor_fails(self, client, auth_headers):
        """Test that donors cannot claim donations."""
        response = client.post("/api/donations/1/claim", headers=auth_headers)
        assert response.status_code == 403  # Forbidden

    def test_claim_nonexistent_donation(self, client, test_shelter_data):
        """Test claiming non-existent donation."""
        # Create shelter and shelter staff user
        client.post("/api/shelters", json=test_shelter_data)
        shelter_user_data = {
            "email": "shelter@example.com",
            "password": "TestPassword123!",
            "name": "Shelter Staff",
            "role": "shelter_staff",
            "shelter_id": 1
        }
        reg_response = client.post("/api/auth/register", json=shelter_user_data)
        shelter_token = reg_response.json()["access_token"]
        shelter_headers = {"Authorization": f"Bearer {shelter_token}"}

        response = client.post("/api/donations/99999/claim", headers=shelter_headers)
        assert response.status_code == 404
