#!/usr/bin/env python3
"""
Seed the database with sample data for testing and development.
Run with: docker compose exec web uv run python scripts/seed_database.py
"""
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.core.auth import get_password_hash
from app.models.user import User, UserRole
from app.models.shelter import Shelter
from app.models.donation import Donation
from app.models.route import Route, Pickup, RouteStatus, PickupStatus


# Status constants for donations (no enum defined)
class DonationStatus:
    AVAILABLE = "available"
    CLAIMED = "claimed"
    COMPLETED = "completed"
    PICKED_UP = "picked_up"


def seed_database():
    """Seed the database with sample data."""
    print("🌱 Seeding database...")

    # Create database session
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"⚠️  Database already has {existing_users} users. Skipping seed.")
            return

        # Create Users
        print("📝 Creating users...")
        users = []

        # Admin
        admin = User(
            email="admin@shelterpickup.org",
            hashed_password=get_password_hash("admin123"),
            name="System Admin",
            phone="555-0001",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        )
        users.append(admin)

        # Donors
        donors_data = [
            {
                "email": "john.doe@example.com",
                "password": "donor123",
                "name": "John Doe",
                "phone": "555-1001",
            },
            {
                "email": "jane.smith@example.com",
                "password": "donor123",
                "name": "Jane Smith",
                "phone": "555-1002",
            },
            {
                "email": "bob.wilson@example.com",
                "password": "donor123",
                "name": "Bob Wilson",
                "phone": "555-1003",
            },
        ]

        for donor_data in donors_data:
            donor = User(
                email=donor_data["email"],
                hashed_password=get_password_hash(donor_data["password"]),
                name=donor_data["name"],
                phone=donor_data["phone"],
                role=UserRole.DONOR,
                is_active=True,
                is_verified=True
            )
            users.append(donor)

        db.add_all(users)
        db.flush()  # Get IDs without committing

        # Create Shelters
        print("🏠 Creating shelters...")
        shelters = []

        shelters_data = [
            {
                "name": "Downtown Women's Shelter",
                "contact_name": "Maria Garcia",
                "email": "contact@downtownshelter.org",
                "phone": "555-2001",
                "address": "123 Main St",
                "city": "Chicago",
                "state": "IL",
                "zip_code": "60601",
                "latitude": "41.8781",
                "longitude": "-87.6298",
                "description": "Emergency shelter for women and children. 50 beds available.",
                "needed_items_text": "blankets, towels, toiletries, canned food",
            },
            {
                "name": "Harbor Light Center",
                "contact_name": "James Johnson",
                "email": "info@harborlight.org",
                "phone": "555-2002",
                "address": "456 Lake Shore Dr",
                "city": "Chicago",
                "state": "IL",
                "zip_code": "60611",
                "latitude": "41.8827",
                "longitude": "-87.6233",
                "description": "Full-service shelter for men. 100 beds, meal service, job placement assistance.",
                "needed_items_text": "winter coats, boots, gloves, hats",
            },
            {
                "name": "Youth Emergency Services",
                "contact_name": "Sarah Chen",
                "email": "help@yes.org",
                "phone": "555-2003",
                "address": "789 W Belmont Ave",
                "city": "Chicago",
                "state": "IL",
                "zip_code": "60657",
                "latitude": "41.9409",
                "longitude": "-87.6533",
                "description": "Emergency services for youth aged 18-24.",
                "needed_items_text": "backpacks, school supplies, hygiene products",
            },
        ]

        for shelter_data in shelters_data:
            shelter = Shelter(**shelter_data)
            shelters.append(shelter)

        db.add_all(shelters)
        db.flush()

        # Create shelter staff users
        print("👤 Creating shelter staff...")
        staff_domains = ["downtown.org", "harbor.org", "youth.org"]
        for i, shelter in enumerate(shelters):
            staff = User(
                email=f"staff{i+1}@{staff_domains[i]}",
                hashed_password=get_password_hash("staff123"),
                name=shelter.contact_name,
                phone=shelter.phone,
                role=UserRole.SHELTER_STAFF,
                shelter_id=shelter.id,
                is_active=True,
                is_verified=True
            )
            db.add(staff)

        db.flush()

        # Create Donations
        print("🎁 Creating donations...")
        donations = []

        donations_data = [
            {
                "donor_name": "John Doe",
                "donor_email": "john.doe@example.com",
                "donor_phone": "555-1001",
                "address": "321 Oak Street",
                "city": "Chicago",
                "state": "IL",
                "zip_code": "60614",
                "latitude": "41.9100",
                "longitude": "-87.6700",
                "items_text": "winter coats (3), blankets (5), warm socks (10 pairs)",
                "notes": "Coats are men's size L and XL. Please pickup by weekend.",
                "status": DonationStatus.AVAILABLE,
            },
            {
                "donor_name": "Jane Smith",
                "donor_email": "jane.smith@example.com",
                "donor_phone": "555-1002",
                "address": "654 Maple Ave",
                "city": "Chicago",
                "state": "IL",
                "zip_code": "60622",
                "latitude": "41.9200",
                "longitude": "-87.6800",
                "items_text": "canned goods (20 cans), rice (5 lbs), pasta (3 boxes)",
                "notes": "All non-perishable. Can pickup anytime.",
                "status": DonationStatus.AVAILABLE,
            },
            {
                "donor_name": "Bob Wilson",
                "donor_email": "bob.wilson@example.com",
                "donor_phone": "555-1003",
                "address": "987 Pine Road",
                "city": "Chicago",
                "state": "IL",
                "zip_code": "60647",
                "latitude": "41.9300",
                "longitude": "-87.6900",
                "items_text": "towels (10), bed sheets (5 sets), pillows (3)",
                "notes": "Moving sale - all in good condition.",
                "status": DonationStatus.CLAIMED,
                "claimed_by_id": shelters[0].id,
            },
            {
                "donor_name": "Anonymous",
                "donor_email": "anonymous@example.com",
                "donor_phone": "555-9999",
                "address": "147 Elm Street",
                "city": "Chicago",
                "state": "IL",
                "zip_code": "60613",
                "latitude": "41.9000",
                "longitude": "-87.6600",
                "items_text": "children's clothes (various sizes 2T-8), toys",
                "notes": "Kids outgrew these. Hope they can help someone.",
                "status": DonationStatus.AVAILABLE,
            },
            {
                "donor_name": "Green Valley Church",
                "donor_email": "donations@greenvalley.org",
                "donor_phone": "555-3001",
                "address": "456 Church Lane",
                "city": "Chicago",
                "state": "IL",
                "zip_code": "60618",
                "latitude": "41.9150",
                "longitude": "-87.6650",
                "items_text": "blankets (20), sleeping bags (10), warm clothing",
                "notes": "Annual winter collection. Large quantity available.",
                "status": DonationStatus.AVAILABLE,
            },
        ]

        for donation_data in donations_data:
            donation = Donation(**donation_data)
            donations.append(donation)

        db.add_all(donations)
        db.flush()

        # Create a sample Route with Pickups
        print("🚚 Creating route with pickups...")
        route = Route(
            name="North Side Pickup Route",
            shelter_id=shelters[0].id,  # Downtown Women's Shelter
            driver_user_id=users[1].id,  # John Doe
            scheduled_date=datetime(2026, 2, 20, 9, 0, 0),
            status=RouteStatus.PLANNED,
            description="Morning pickup route - start at 9 AM"
        )
        db.add(route)
        db.flush()

        # Add pickups to the route
        pickup_data = [
            {
                "route_id": route.id,
                "donation_id": donations[0].id,
                "sequence_order": 1,
                "status": PickupStatus.PENDING,
                "notes": "First stop - morning pickup"
            },
            {
                "route_id": route.id,
                "donation_id": donations[1].id,
                "sequence_order": 2,
                "status": PickupStatus.PENDING,
                "notes": "Second stop"
            },
            {
                "route_id": route.id,
                "donation_id": donations[3].id,
                "sequence_order": 3,
                "status": PickupStatus.PENDING,
                "notes": "Final stop - afternoon pickup"
            },
        ]

        for pickup in pickup_data:
            db.add(Pickup(**pickup))

        # Commit all changes
        db.commit()

        print("\n✅ Database seeded successfully!")
        print("\n📊 Summary:")
        print(f"   Users: {db.query(User).count()}")
        print(f"   Shelters: {db.query(Shelter).count()}")
        print(f"   Donations: {db.query(Donation).count()}")
        print(f"   Routes: {db.query(Route).count()}")
        print(f"   Pickups: {db.query(Pickup).count()}")

        print("\n🔐 Test Credentials:")
        print("   Admin: admin@shelterpickup.org / admin123")
        print("   Donor: john.doe@example.com / donor123")
        print("   Donor: jane.smith@example.com / donor123")
        print(f"   Staff 1: staff1@downtown.org / staff123")
        print(f"   Staff 2: staff2@harbor.org / staff123")

    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
