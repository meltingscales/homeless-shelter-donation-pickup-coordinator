# Deployment Guide

## Development Setup

```bash
# Install dependencies
pip install -e .

# Run with SQLite (no PostGIS needed)
export USE_POSTGIS=false
uvicorn main:app --reload

# Visit http://localhost:8000
# API docs: http://localhost:8000/docs
```

## Production Deployment

### Option 1: Docker Compose (Recommended for PostGIS)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

### Option 2: Render (PostgreSQL + PostGIS)

1. Create a new PostgreSQL + PostGIS database on Render
2. Set environment variables:
   - `USE_POSTGIS=true`
   - `DATABASE_URL=postgresql://...`
   - `SECRET_KEY` (generate with `openssl rand -hex 32`)
3. Deploy via GitHub connection

### Option 3: Railway

1. Create a new project
2. Add PostgreSQL service
3. Enable PostGIS extension in Railway
4. Deploy with build command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Option 4: Traditional VPS

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3.11 python3-pip postgresql postgis

# Clone repo
git clone <your-repo>
cd <repo>

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run with gunicorn (production)
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Systemd Service (Linux)

Create `/etc/systemd/system/shelter-pickup.service`:

```ini
[Unit]
Description=Shelter Pickup Coordinator
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/shelter-pickup
Environment="PATH=/var/www/shelter-pickup/venv/bin"
ExecStart=/var/www/shelter-pickup/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable shelter-pickup
sudo systemctl start shelter-pickup
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `USE_POSTGIS` | Enable PostGIS | No | `true` |
| `DATABASE_URL` | PostgreSQL connection | Yes* | - |
| `SQLITE_URL` | SQLite fallback path | No | `./shelter.db` |
| `SECRET_KEY` | JWT signing key | Yes | - |
| `GOOGLE_MAPS_API_KEY` | For geocoding | No | - |

*Required if `USE_POSTGIS=true`

## Health Check

```bash
curl http://localhost:8000/docs
```

## Backup & Restore

### PostgreSQL

```bash
# Backup
pg_dump -U shelter_user shelter_pickup > backup.sql

# Restore
psql -U shelter_user shelter_pickup < backup.sql
```

### SQLite

```bash
# Backup
cp shelter.db shelter.db.backup

# Restore
cp shelter.db.backup shelter.db
```
