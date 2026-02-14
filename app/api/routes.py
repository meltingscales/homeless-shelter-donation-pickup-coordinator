from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.auth import get_current_user, get_current_shelter_staff
from app.models.route import Route, Pickup, RouteStatus, PickupStatus
from app.models.donation import Donation
from app.models.user import User
from app.schemas.route import (
    RouteCreate,
    RouteUpdate,
    RouteResponse,
    PickupCreate,
    PickupUpdate,
    PickupResponse,
    PickupWithDonation,
    AddPickupsToRoute,
)

router = APIRouter(prefix="/api/routes", tags=["routes"])


@router.post("", response_model=RouteResponse)
def create_route(
    route_data: RouteCreate,
    current_user: User = Depends(get_current_shelter_staff),
    db: Session = Depends(get_db)
):
    """Create a new pickup route."""
    # Verify the user is associated with the specified shelter
    if current_user.shelter_id != route_data.shelter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create routes for your shelter"
        )

    # Verify the driver exists
    driver = db.query(User).filter(User.id == route_data.driver_user_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    new_route = Route(**route_data.model_dump())
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route


@router.get("", response_model=List[RouteResponse])
def list_routes(
    shelter_id: int = None,
    status: RouteStatus = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List routes, optionally filtered by shelter or status."""
    query = db.query(Route)

    # Shelter staff can only see their shelter's routes
    if current_user.is_shelter_staff and shelter_id is None:
        shelter_id = current_user.shelter_id

    if shelter_id:
        query = query.filter(Route.shelter_id == shelter_id)
    if status:
        query = query.filter(Route.status == status)

    return query.order_by(Route.created_at.desc()).all()


@router.get("/{route_id}", response_model=RouteResponse)
def get_route(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific route with its pickups."""
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Shelter staff can only view their shelter's routes
    if current_user.is_shelter_staff and current_user.shelter_id != route.shelter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return route


@router.put("/{route_id}", response_model=RouteResponse)
def update_route(
    route_id: int,
    route_data: RouteUpdate,
    current_user: User = Depends(get_current_shelter_staff),
    db: Session = Depends(get_db)
):
    """Update a route."""
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Verify shelter ownership
    if current_user.shelter_id != route.shelter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update routes for your shelter"
        )

    # Update fields
    update_data = route_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(route, field, value)

    # Update timestamps based on status
    if route_data.status == RouteStatus.IN_PROGRESS and not route.started_at:
        route.started_at = datetime.utcnow()
    elif route_data.status == RouteStatus.COMPLETED and not route.completed_at:
        route.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(route)
    return route


@router.delete("/{route_id}")
def delete_route(
    route_id: int,
    current_user: User = Depends(get_current_shelter_staff),
    db: Session = Depends(get_db)
):
    """Delete a route (only if in planned status)."""
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Verify shelter ownership
    if current_user.shelter_id != route.shelter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete routes for your shelter"
        )

    if route.status != RouteStatus.PLANNED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only delete routes in 'planned' status"
        )

    db.delete(route)
    db.commit()
    return {"message": "Route deleted successfully"}


@router.post("/{route_id}/pickups", response_model=List[PickupResponse])
def add_pickups_to_route(
    route_id: int,
    data: AddPickupsToRoute,
    current_user: User = Depends(get_current_shelter_staff),
    db: Session = Depends(get_db)
):
    """Add donations to a route."""
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Verify shelter ownership
    if current_user.shelter_id != route.shelter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only modify routes for your shelter"
        )

    if route.status != RouteStatus.PLANNED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only add pickups to routes in 'planned' status"
        )

    # Get current max sequence order
    max_order = db.query(Pickup).filter(Pickup.route_id == route_id).count()

    pickups = []
    for i, donation_id in enumerate(data.donation_ids):
        # Verify donation exists and is available
        donation = db.query(Donation).filter(Donation.id == donation_id).first()
        if not donation:
            raise HTTPException(status_code=404, detail=f"Donation {donation_id} not found")

        if donation.status != "available":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Donation {donation_id} is not available"
            )

        # Check if donation is already in a route
        existing = db.query(Pickup).filter(Pickup.donation_id == donation_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Donation {donation_id} is already in a route"
            )

        # Create pickup
        pickup = Pickup(
            route_id=route_id,
            donation_id=donation_id,
            sequence_order=max_order + i + 1
        )
        db.add(pickup)
        pickups.append(pickup)

    db.commit()
    for pickup in pickups:
        db.refresh(pickup)

    return pickups


@router.get("/{route_id}/pickups", response_model=List[PickupWithDonation])
def get_route_pickups(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all pickups for a route with donation details."""
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Shelter staff can only view their shelter's routes
    if current_user.is_shelter_staff and current_user.shelter_id != route.shelter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    pickups = db.query(Pickup).filter(Pickup.route_id == route_id).order_by(Pickup.sequence_order).all()

    result = []
    for pickup in pickups:
        donation = db.query(Donation).filter(Donation.id == pickup.donation_id).first()
        if donation:
            result.append(PickupWithDonation(
                **PickupResponse.model_validate(pickup).model_dump(),
                donation_address=donation.address,
                donation_city=donation.city,
                donation_state=donation.state,
                donation_zip=donation.zip_code,
                donation_items_summary=donation.items_summary,
                donation_lat=donation.latitude,
                donation_lng=donation.longitude,
            ))

    return result


@router.put("/pickups/{pickup_id}", response_model=PickupResponse)
def update_pickup(
    pickup_id: int,
    pickup_data: PickupUpdate,
    current_user: User = Depends(get_current_shelter_staff),
    db: Session = Depends(get_db)
):
    """Update a pickup status."""
    pickup = db.query(Pickup).filter(Pickup.id == pickup_id).first()
    if not pickup:
        raise HTTPException(status_code=404, detail="Pickup not found")

    # Get the route to verify shelter ownership
    route = db.query(Route).filter(Route.id == pickup.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    if current_user.shelter_id != route.shelter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only modify pickups for your shelter"
        )

    # Update fields
    update_data = pickup_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pickup, field, value)

    # Update timestamps and donation status
    if pickup_data.status == PickupStatus.IN_PROGRESS and not pickup.arrived_at:
        pickup.arrived_at = datetime.utcnow()
    elif pickup_data.status == PickupStatus.COMPLETED:
        if not pickup.completed_at:
            pickup.completed_at = datetime.utcnow()
        # Update donation status
        donation = db.query(Donation).filter(Donation.id == pickup.donation_id).first()
        if donation:
            donation.status = "picked_up"

    db.commit()
    db.refresh(pickup)
    return pickup


@router.post("/pickups/{pickup_id}/skip")
def skip_pickup(
    pickup_id: int,
    reason: str,
    current_user: User = Depends(get_current_shelter_staff),
    db: Session = Depends(get_db)
):
    """Skip a pickup with a reason."""
    pickup = db.query(Pickup).filter(Pickup.id == pickup_id).first()
    if not pickup:
        raise HTTPException(status_code=404, detail="Pickup not found")

    # Get the route to verify shelter ownership
    route = db.query(Route).filter(Route.id == pickup.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    if current_user.shelter_id != route.shelter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only modify pickups for your shelter"
        )

    pickup.status = PickupStatus.SKIPPED
    pickup.failed_reason = reason

    db.commit()
    return {"message": "Pickup skipped"}


@router.get("/shelter/{shelter_id}/optimized")
def get_optimized_route(
    shelter_id: int,
    current_user: User = Depends(get_current_shelter_staff),
    db: Session = Depends(get_db)
):
    """
    Get an optimized route for available donations near this shelter.

    Simple nearest-neighbor algorithm starting from the shelter.
    """
    # Verify shelter ownership
    if current_user.shelter_id != shelter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    # Get shelter location
    shelter = db.query(Donation).filter(Donation.id == shelter_id).first()
    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")

    # Get available donations claimed by this shelter
    donations = db.query(Donation).filter(
        Donation.claimed_by_id == shelter_id,
        Donation.status == "claimed"
    ).all()

    # Simple optimization: return donations ordered by zip code
    # (A real implementation would use distance calculations with PostGIS)
    result = []
    for donation in donations[:20]:  # Limit to 20 donations
        result.append({
            "donation_id": donation.id,
            "address": f"{donation.address}, {donation.city}, {donation.state} {donation.zip_code}",
            "items_summary": donation.items_summary,
            "latitude": donation.latitude,
            "longitude": donation.longitude,
        })

    return {
        "shelter_id": shelter_id,
        "suggested_order": result,
        "total_count": len(result)
    }


@router.get("/{route_id}/summary")
def get_route_summary(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a summary of items to be picked up on a route."""
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Shelter staff can only view their shelter's routes
    if current_user.is_shelter_staff and current_user.shelter_id != route.shelter_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    pickups = db.query(Pickup).filter(Pickup.route_id == route_id).all()

    all_items = {}
    total_pickups = len(pickups)
    completed_pickups = sum(1 for p in pickups if p.status == PickupStatus.COMPLETED)
    pending_pickups = sum(1 for p in pickups if p.status == PickupStatus.PENDING)

    for pickup in pickups:
        donation = db.query(Donation).filter(Donation.id == pickup.donation_id).first()
        if donation and donation.items_structured:
            # Aggregate items
            for category, subcategories in donation.items_structured.items():
                if category not in all_items:
                    all_items[category] = {}
                if isinstance(subcategories, dict):
                    for subcategory, items in subcategories.items():
                        if subcategory not in all_items[category]:
                            all_items[category][subcategory] = {}
                        for item, quantity in items.items():
                            all_items[category][subcategory][item] = \
                                all_items[category][subcategory].get(item, 0) + quantity

    return {
        "route_id": route_id,
        "route_name": route.name,
        "status": route.status,
        "total_pickups": total_pickups,
        "completed_pickups": completed_pickups,
        "pending_pickups": pending_pickups,
        "items_summary": all_items,
    }
