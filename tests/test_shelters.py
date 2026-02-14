"""
Tests for shelter endpoints.
"""
import pytest


class TestSheltersCreate:
    """Tests for creating shelters."""

    def test_create_shelter(self, client, test_shelter_data):
        """Test creating a shelter."""
        response = client.post("/api/shelters", json=test_shelter_data)
        assert response.status_code == 200

        data = response.json()
        assert data["name"] == test_shelter_data["name"]
        assert data["email"] == test_shelter_data["email"]

    def test_create_shelter_duplicate_name(self, client, test_shelter_data):
        """Test creating shelter with duplicate name fails."""
        # First shelter
        client.post("/api/shelters", json=test_shelter_data)

        # Second shelter with same name
        response = client.post("/api/shelters", json=test_shelter_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    def test_create_shelter_with_structured_needs(self, client, test_shelter_data):
        """Test creating shelter with structured needed items."""
        test_shelter_data["needed_items_structured"] = {
            "clothing": {
                "winter": {"coats": 10, "blankets": 5}
            }
        }

        response = client.post("/api/shelters", json=test_shelter_data)
        assert response.status_code == 200

        data = response.json()
        assert data["needed_items_structured"]["clothing"]["winter"]["coats"] == 10


class TestSheltersList:
    """Tests for listing shelters."""

    def test_list_shelters(self, client, test_shelter_data):
        """Test listing all shelters."""
        # Create a shelter
        client.post("/api/shelters", json=test_shelter_data)

        # List shelters
        response = client.get("/api/shelters")
        assert response.status_code == 200

        data = response.json()
        assert len(data) >= 1


class TestSheltersGet:
    """Tests for getting a specific shelter."""

    def test_get_shelter(self, client, test_shelter_data):
        """Test getting a specific shelter."""
        # Create a shelter
        create_response = client.post("/api/shelters", json=test_shelter_data)
        shelter_id = create_response.json()["id"]

        # Get the shelter
        response = client.get(f"/api/shelters/{shelter_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == shelter_id
        assert data["name"] == test_shelter_data["name"]

    def test_get_shelter_not_found(self, client):
        """Test getting non-existent shelter."""
        response = client.get("/api/shelters/99999")
        assert response.status_code == 404


class TestSheltersNearby:
    """Tests for finding nearby shelters."""

    def test_nearby_shelters(self, client, test_shelter_data):
        """Test finding shelters near a location."""
        # Create a shelter
        client.post("/api/shelters", json=test_shelter_data)

        # Find nearby (Chicago coordinates)
        response = client.get("/api/shelters/nearby?lat=41.8781&lng=-87.6298&radius_miles=50")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
