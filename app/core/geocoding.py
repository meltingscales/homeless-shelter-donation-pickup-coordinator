"""
Geocoding utilities for converting addresses to coordinates.

Uses Google Maps Geocoding API (requires API key).
"""
import os
from typing import Tuple, Optional
import requests


# TODO: Set this environment variable or add to config.py
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")


def geocode_address(address: str, city: str, state: str, zip_code: str) -> Optional[Tuple[float, float]]:
    """
    Convert an address to (latitude, longitude) using Google Maps Geocoding API.

    Args:
        address: Street address
        city: City name
        state: State abbreviation (2 letters)
        zip_code: ZIP code

    Returns:
        (latitude, longitude) tuple or None if geocoding fails
    """
    if not GOOGLE_MAPS_API_KEY:
        # For development, return None without making API call
        return None

    # Build the full address string
    full_address = f"{address}, {city}, {state} {zip_code}"

    # Call Google Maps Geocoding API
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": full_address,
        "key": GOOGLE_MAPS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "OK" and data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return (location["lat"], location["lng"])

        return None
    except (requests.RequestException, KeyError, ValueError):
        return None


def geocode_and_update(model_instance) -> bool:
    """
    Geocode the address fields of a model instance and update its location.

    Args:
        model_instance: A Donation or Shelter instance

    Returns:
        True if geocoding succeeded, False otherwise
    """
    if not GOOGLE_MAPS_API_KEY:
        return False

    result = geocode_address(
        address=model_instance.address,
        city=model_instance.city,
        state=model_instance.state,
        zip_code=model_instance.zip_code,
    )

    if result:
        model_instance.latitude = str(result[0])
        model_instance.longitude = str(result[1])
        return True

    return False
