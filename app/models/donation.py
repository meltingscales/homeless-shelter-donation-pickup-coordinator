from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.config import settings

# Import GeoAlchemy2 for PostGIS support
if settings.USE_POSTGIS:
    from geoalchemy2 import Geometry


class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Donor info
    donor_name = Column(String(200), nullable=False)
    donor_email = Column(String(200), nullable=False)
    donor_phone = Column(String(50), nullable=True)

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

    # Donation details
    items = Column(Text, nullable=False)  # Free-text description of items
    notes = Column(Text, nullable=True)

    # Status
    status = Column(String(20), default="available")  # available, claimed, completed

    # If claimed, which shelter?
    claimed_by_id = Column(Integer, ForeignKey("shelters.id"), nullable=True)
    claimed_by = relationship("Shelter", back_populates="claimed_donations")
    claimed_at = Column(DateTime, nullable=True)

    @property
    def lat_lng(self):
        """Return (lat, lng) tuple."""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None

    def __repr__(self):
        return f"<Donation {self.id}: {self.items[:30]}... from {self.zip_code}>"
