from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any


class DonationCreate(BaseModel):
    donor_name: str
    donor_email: EmailStr
    donor_phone: str | None = None
    address: str
    city: str
    state: str  # Should be 2-letter state code
    zip_code: str
    # Items can be structured (JSON) or simple text
    items_structured: Optional[Dict[str, Any]] = None
    items_text: Optional[str] = None
    notes: str | None = None


class DonationResponse(BaseModel):
    id: int
    created_at: datetime
    donor_name: str
    donor_email: str
    donor_phone: str | None
    address: str
    city: str
    state: str
    zip_code: str
    latitude: str | None
    longitude: str | None
    items_structured: Optional[Dict[str, Any]] = None
    items_text: Optional[str] = None
    items_summary: str  # Computed property
    has_structured_items: bool  # Computed property
    notes: str | None
    status: str
    claimed_by_id: int | None
    claimed_at: datetime | None

    class Config:
        from_attributes = True
