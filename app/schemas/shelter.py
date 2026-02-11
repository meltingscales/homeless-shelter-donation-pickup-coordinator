from datetime import datetime
from pydantic import BaseModel, EmailStr, HttpUrl


class ShelterCreate(BaseModel):
    name: str
    contact_name: str
    email: EmailStr
    phone: str | None = None
    address: str
    city: str
    state: str  # Should be 2-letter state code
    zip_code: str
    description: str | None = None
    website: str | None = None
    needed_items: str | None = None


class ShelterResponse(BaseModel):
    id: int
    created_at: datetime
    name: str
    contact_name: str
    email: str
    phone: str | None
    address: str
    city: str
    state: str
    zip_code: str
    latitude: str | None
    longitude: str | None
    description: str | None
    website: str | None
    needed_items: str | None

    class Config:
        from_attributes = True
