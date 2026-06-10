from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
import models  # noqa: F401
from service import BookingService
from schemas import BookingCreate, BookingOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Booking Service", version="1.0.0")


def get_service(db: Session = Depends(get_db)) -> BookingService:
    return BookingService(db)


@app.get("/health")
def health():
    return {"status": "ok", "service": "booking"}


@app.get("/bookings", response_model=list[BookingOut])
def list_bookings(svc: BookingService = Depends(get_service)):
    return svc.list_bookings()


@app.post("/bookings", response_model=BookingOut, status_code=201)
def create_booking(payload: BookingCreate, svc: BookingService = Depends(get_service)):
    return svc.create_booking(payload)
