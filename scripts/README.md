# Scripts

This directory contains utility scripts for the Shelter Pickup Coordinator application.

## seed_database.py

Populates the database with sample test data including:
- 1 Admin user
- 3 Donor users
- 3 Shelters
- 3 Shelter staff users
- 5 Donations (various statuses)
- 1 Route with 3 Pickups

### Usage

Run from within the Docker container:

```bash
docker compose exec web uv run python scripts/seed_database.py
```

### Test Credentials

After running the seed script, you can log in with these test accounts:

**Admin:**
- Email: `admin@shelterpickup.org`
- Password: `admin123`

**Donors:**
- Email: `john.doe@example.com` / Password: `donor123`
- Email: `jane.smith@example.com` / Password: `donor123`
- Email: `bob.wilson@example.com` / Password: `donor123`

**Shelter Staff:**
- Email: `staff1@downtownwomens.org` / Password: `staff123`
- Email: `staff2@harborlight.org` / Password: `staff123`
- Email: `staff3@youth.org` / Password: `staff123`

### Resetting the Database

To reset the database and reseed:

```bash
docker compose down -v  # Removes all volumes
docker compose up -d --build
docker compose exec web uv run python scripts/seed_database.py
```
