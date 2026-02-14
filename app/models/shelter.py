from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.config import settings

# Import GeoAlchemy2 for PostGIS support
if settings.USE_POSTGIS:
    from geoalchemy2 import Geometry


class Shelter(Base):
    __tablename__ = "shelters"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Shelter info
    name = Column(String(200), nullable=False, unique=True)
    contact_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(50), nullable=True)

    # Location (keep address fields for geocoding/display)
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(10), nullable=False, index=True)

    # Geospatial location (PostGIS Point: longitude, latitude)
    if settings.USE_POSTGIS:
        location = Column(Geometry('POINT', srid=4326, spatial_index=True), nullable=True)
        latitude = Column(String(20), nullable=True)  # Cache for easy access
        longitude = Column(String(20), nullable=True)
    else:
        # SQLite fallback
        latitude = Column(String(20), nullable=True)
        longitude = Column(String(20), nullable=True)

    # Public info
    description = Column(Text, nullable=True)
    website = Column(String(500), nullable=True)

    # What items they need - structured (JSON) or free-text
    needed_items_structured = Column(JSON, nullable=True)  # {"food": {"produce": {"lettuce": 10}}}
    needed_items_text = Column(Text, nullable=True)  # Fallback for simple text

    # Relationships
    claimed_donations = relationship("Donation", back_populates="claimed_by")

    @property
    def lat_lng(self):
        """Return (lat, lng) tuple."""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None

    @property
    def has_structured_needs(self) -> bool:
        """Check if this shelter has structured needed items."""
        return self.needed_items_structured is not None

    @property
    def needs_summary(self) -> str:
        """Get a summary of needed items for display."""
        if self.needed_items_structured:
            from app.core.items import get_item_summary
            summary = get_item_summary(self.needed_items_structured)
            return ", ".join(summary[:10])  # Limit to first 10 items
        return self.needed_items_text or "No specific needs listed"

    def find_matching_donations(self, donations: list) -> list:
        """Find donations that match this shelter's needs."""
        if not self.needed_items_structured:
            return []

        matches = []
        from app.core.items import find_matching_items

        for donation in donations:
            if donation.status != "available":
                continue
            if not donation.items_structured:
                continue

            matching = find_matching_items(self.needed_items_structured, donation.items_structured)
            if matching:
                matches.append({
                    "donation": donation,
                    "matches": matching
                })

        return matches

    def __repr__(self):
        return f"<Shelter {self.id}: {self.name}>"
