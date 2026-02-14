from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.route import RouteStatus, PickupStatus


# Request schemas
class RouteCreate(BaseModel):
    name: str
    description: Optional[str] = None
    shelter_id: int
    driver_user_id: int
    scheduled_date: Optional[datetime] = None


class RouteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[RouteStatus] = None
    scheduled_date: Optional[datetime] = None


class PickupCreate(BaseModel):
    donation_id: int
    sequence_order: int


class PickupUpdate(BaseModel):
    status: Optional[PickupStatus] = None
    notes: Optional[str] = None
    failed_reason: Optional[str] = None


class AddPickupsToRoute(BaseModel):
    donation_ids: List[int]  # Will be added in sequence order


# Response schemas
class PickupResponse(BaseModel):
    id: int
    route_id: int
    donation_id: int
    sequence_order: int
    status: PickupStatus
    notes: Optional[str]
    failed_reason: Optional[str]
    arrived_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class PickupWithDonation(PickupResponse):
    """Pickup with donation details included."""
    donation_address: str
    donation_city: str
    donation_state: str
    donation_zip: str
    donation_items_summary: str
    donation_lat: Optional[str] = None
    donation_lng: Optional[str] = None


class RouteResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    shelter_id: int
    driver_user_id: int
    status: RouteStatus
    scheduled_date: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    pickups: List[PickupResponse] = []

    class Config:
        from_attributes = True
