from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.config import settings
from app.models.shelter import Shelter
from app.schemas.shelter import ShelterCreate, ShelterResponse

router = APIRouter(prefix="/api/shelters", tags=["shelters"])

# Import GeoAlchemy2 for PostGIS spatial queries
if settings.USE_POSTGIS:
    from geoalchemy2 import functions as geofunc
    from geoalchemy2.elements import WKTElement


@router.post("", response_model=ShelterResponse)
def create_shelter(shelter: ShelterCreate, db: Session = Depends(get_db)):
    """Register a new shelter."""
    # Check if shelter with this name already exists
    existing = db.query(Shelter).filter(Shelter.name == shelter.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Shelter with this name already exists")

    db_shelter = Shelter(**shelter.model_dump())
    db.add(db_shelter)
    db.commit()
    db.refresh(db_shelter)
    return db_shelter


@router.get("", response_model=List[ShelterResponse])
def list_shelters(db: Session = Depends(get_db)):
    """List all shelters."""
    return db.query(Shelter).order_by(Shelter.name).all()


@router.get("/nearby", response_model=List[ShelterResponse])
def list_nearby_shelters(
    lat: float,
    lng: float,
    radius_miles: float = 50,
    db: Session = Depends(get_db)
):
    """
    Find shelters near a location.

    Args:
        lat: Latitude of the center point
        lng: Longitude of the center point
        radius_miles: Search radius in miles (default: 50)

    Returns:
        List of shelters within the search radius
    """
    if not settings.USE_POSTGIS:
        # Fallback for SQLite: return all shelters
        return db.query(Shelter).order_by(Shelter.name).all()

    # PostGIS spatial query
    radius_degrees = radius_miles / 69.0
    point = WKTElement(f'POINT({lng} {lat})', srid=4326)

    query = db.query(Shelter).filter(
        geofunc.ST_DWithin(
            Shelter.location,
            point,
            radius_degrees
        )
    )

    # Order by distance
    query = query.order_by(
        geofunc.ST_Distance(Shelter.location, point)
    )

    return query.all()


@router.get("/{shelter_id}", response_model=ShelterResponse)
def get_shelter(shelter_id: int, db: Session = Depends(get_db)):
    """Get a specific shelter by ID."""
    shelter = db.query(Shelter).filter(Shelter.id == shelter_id).first()
    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")
    return shelter
