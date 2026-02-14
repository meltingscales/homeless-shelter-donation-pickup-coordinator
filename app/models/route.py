from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.core.database import Base


class RouteStatus(str, Enum):
    """Status of a pickup route."""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PickupStatus(str, Enum):
    """Status of a single pickup."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Route details
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    shelter_id = Column(Integer, ForeignKey("shelters.id"), nullable=False)
    driver_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Status
    status = Column(SQLEnum(RouteStatus), default=RouteStatus.PLANNED)

    # Scheduling
    scheduled_date = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    pickups = relationship("Pickup", back_populates="route", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Route {self.id}: {self.name} ({self.status})>"


class Pickup(Base):
    __tablename__ = "pickups"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    donation_id = Column(Integer, ForeignKey("donations.id"), nullable=False)

    # Order in the route sequence
    sequence_order = Column(Integer, nullable=False)

    # Status
    status = Column(SQLEnum(PickupStatus), default=PickupStatus.PENDING)

    # Notes
    notes = Column(Text, nullable=True)
    failed_reason = Column(String(500), nullable=True)  # If skipped/failed

    # Timestamps
    arrived_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    route = relationship("Route", back_populates="pickups")

    def __repr__(self):
        return f"<Pickup {self.id}: Route {self.route_id} -> Donation {self.donation_id}>"
