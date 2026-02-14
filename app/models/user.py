from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.core.database import Base


class UserRole(str, Enum):
    """User roles for access control."""
    DONOR = "donor"           # Can create donations
    SHELTER_STAFF = "shelter_staff"  # Can claim donations for shelter
    ADMIN = "admin"           # Full access


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Authentication
    email = Column(String(200), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)

    # Profile
    name = Column(String(200), nullable=False)
    phone = Column(String(50), nullable=True)

    # Role-based access
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.DONOR)

    # Shelter association (for shelter_staff role)
    shelter_id = Column(Integer, nullable=True)  # FK to shelters table

    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User {self.id}: {self.email} ({self.role})>"

    @property
    def is_donor(self) -> bool:
        return self.role == UserRole.DONOR

    @property
    def is_shelter_staff(self) -> bool:
        return self.role == UserRole.SHELTER_STAFF

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
