from datetime import datetime
from pydantic import BaseModel, EmailStr


class DonationCreate(BaseModel):
    donor_name: str
    donor_email: EmailStr
    donor_phone: str | None = None
    address: str
    city: str
    state: str  # Should be 2-letter state code
    zip_code: str
    items: str  # Description of items being donated
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
    items: str
    notes: str | None
    status: str
    claimed_by_id: int | None
    claimed_at: datetime | None

    class Config:
        from_attributes = True
