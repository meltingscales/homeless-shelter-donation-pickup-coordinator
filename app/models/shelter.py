from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
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

    # What items they need
    needed_items = Column(Text, nullable=True)  # Free-text, e.g. "blankets, coats, socks"

    # Relationships
    claimed_donations = relationship("Donation", back_populates="claimed_by")

    @property
    def lat_lng(self):
        """Return (lat, lng) tuple."""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None

    def __repr__(self):
        return f"<Shelter {self.id}: {self.name}>"
