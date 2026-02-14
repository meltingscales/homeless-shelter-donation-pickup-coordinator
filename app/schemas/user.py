from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


# Request schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.DONOR
    shelter_id: Optional[int] = None  # Required for shelter_staff role


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Response schemas
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    phone: Optional[str]
    role: UserRole
    shelter_id: Optional[int]
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
