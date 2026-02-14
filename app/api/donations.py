from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.core.database import get_db
from app.core.config import settings
from app.core.auth import get_current_user, get_current_shelter_staff
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationResponse

router = APIRouter(prefix="/api/donations", tags=["donations"])

# Import GeoAlchemy2 for PostGIS spatial queries
if settings.USE_POSTGIS:
    from geoalchemy2 import functions as geofunc
    from geoalchemy2.elements import WKTElement


@router.post("", response_model=DonationResponse)
def create_donation(
    donation: DonationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new donation listing (requires authentication)."""
    db_donation = Donation(
        **donation.model_dump(),
        donor_user_id=current_user.id
    )
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)
    return db_donation


@router.get("", response_model=List[DonationResponse])
def list_donations(
    status: str | None = None,
    zip_code: str | None = None,
    db: Session = Depends(get_db)
):
    """List all donations, optionally filtered by status or zip code."""
    query = db.query(Donation)

    if status:
        query = query.filter(Donation.status == status)
    if zip_code:
        query = query.filter(Donation.zip_code == zip_code)

    return query.order_by(Donation.created_at.desc()).all()


@router.get("/nearby", response_model=List[DonationResponse])
def list_nearby_donations(
    lat: float,
    lng: float,
    radius_miles: float = 25,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    """
    Find donations near a location.

    Args:
        lat: Latitude of the center point
        lng: Longitude of the center point
        radius_miles: Search radius in miles (default: 25)
        status: Filter by donation status (optional)

    Returns:
        List of donations within the search radius
    """
    if not settings.USE_POSTGIS:
        # Fallback for SQLite: return all donations (no spatial filtering)
        query = db.query(Donation)
        if status:
            query = query.filter(Donation.status == status)
        return query.order_by(Donation.created_at.desc()).all()

    # PostGIS spatial query
    # Convert miles to degrees (approximate: 1 degree ≈ 69 miles)
    radius_degrees = radius_miles / 69.0

    # Create a point from lat/lng (WKT format: POINT(lng lat))
    point = WKTElement(f'POINT({lng} {lat})', srid=4326)

    # Build query with spatial filter
    query = db.query(Donation).filter(
        geofunc.ST_DWithin(
            Donation.location,
            point,
            radius_degrees
        )
    )

    if status:
        query = query.filter(Donation.status == status)

    # Order by distance and return
    query = query.order_by(
        geofunc.ST_Distance(Donation.location, point)
    )

    return query.all()


@router.get("/my-donations", response_model=List[DonationResponse])
def list_my_donations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List donations created by the current user."""
    return db.query(Donation).filter(
        Donation.donor_user_id == current_user.id
    ).order_by(Donation.created_at.desc()).all()


@router.get("/{donation_id}", response_model=DonationResponse)
def get_donation(donation_id: int, db: Session = Depends(get_db)):
    """Get a specific donation by ID."""
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    return donation


@router.post("/{donation_id}/claim")
def claim_donation(
    donation_id: int,
    current_user: User = Depends(get_current_shelter_staff),
    db: Session = Depends(get_db)
):
    """
    Claim a donation for the current user's shelter.

    Requires shelter_staff role.
    """
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    if donation.status != "available":
        raise HTTPException(status_code=400, detail="Donation is not available")

    # Use the shelter_id from the authenticated user
    from datetime import datetime
    donation.status = "claimed"
    donation.claimed_by_id = current_user.shelter_id
    donation.claimed_at = datetime.utcnow()

    db.commit()
    return {"message": "Donation claimed successfully"}
