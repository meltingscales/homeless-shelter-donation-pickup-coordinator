from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.database import engine, init_postgis
from app.core.config import settings
from app.models import Donation, Shelter
from app.api import donations, shelters

# Create tables
from app.core.database import Base
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shelter Pickup Coordinator",
    description="Simple donation coordination for homeless shelters",
    version="0.1.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    if settings.USE_POSTGIS:
        init_postgis()


# API routes
app.include_router(donations.router)
app.include_router(shelters.router)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return FileResponse("templates/index.html")


@app.get("/donor")
def donor_page():
    return FileResponse("templates/donor.html")


@app.get("/shelter")
def shelter_page():
    return FileResponse("templates/shelter.html")
