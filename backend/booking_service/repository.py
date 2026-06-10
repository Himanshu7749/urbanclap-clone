from sqlalchemy.orm import Session
from models import Booking
from datetime import datetime


class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, provider_id: int, scheduled_at: datetime) -> Booking:
        booking = Booking(
            user_id=user_id,
            provider_id=provider_id,
            scheduled_at=scheduled_at,
            status="pending",
        )
        self.db.add(booking)
        self.db.flush()
        return booking

    def list_all(self) -> list[Booking]:
        return self.db.query(Booking).order_by(Booking.scheduled_at.desc()).all()

    def get_by_id(self, booking_id: int) -> Booking | None:
        return self.db.query(Booking).filter(Booking.id == booking_id).first()
