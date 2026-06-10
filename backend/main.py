from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from database import engine, get_db
from models import Base, Service, Provider, User, Booking
from schemas import (
    ServiceWithProviders,
    ProviderWithService,
    BookingOut,
    BookingCreate,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="UrbanServe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/services/{slug}", response_model=ServiceWithProviders)
def get_service(slug: str, db: Session = Depends(get_db)):
    """Return a service and all its providers by slug."""
    service = db.query(Service).filter(Service.slug == slug).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@app.get("/api/providers/{provider_id}", response_model=ProviderWithService)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    """Return a single provider with their service info by ID."""
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


@app.get("/api/bookings", response_model=list[BookingOut])
def list_bookings(db: Session = Depends(get_db)):
    """Return all bookings ordered by scheduled_at descending."""
    return (
        db.query(Booking)
        .join(Booking.provider)
        .join(Booking.user)
        .order_by(Booking.scheduled_at.desc())
        .all()
    )


@app.post("/api/bookings", response_model=BookingOut, status_code=201)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    """
    Create a booking.
    - Upserts the user by email (creates if new, updates name if existing).
    - Validates that the provider exists.
    - Creates the Booking record with status 'pending'.
    """
    provider = db.query(Provider).filter(Provider.id == payload.provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    user = db.query(User).filter(User.email == payload.email).first()
    if user:
        user.name = payload.name
    else:
        user = User(name=payload.name, email=payload.email)
        db.add(user)
    db.flush()

    try:
        scheduled_at = datetime.fromisoformat(payload.scheduled_at)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid scheduledAt format")

    booking = Booking(
        user_id=user.id,
        provider_id=provider.id,
        scheduled_at=scheduled_at,
        status="pending",
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
