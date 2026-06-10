import os
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
import httpx

from repository import BookingRepository
from clients import upsert_user, get_provider, send_booking_confirmation
from schemas import BookingOut, BookingCreate, UserInfo

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8001")


class BookingService:
    def __init__(self, db: Session):
        self.repo = BookingRepository(db)
        self.db = db

    def _fetch_user(self, user_id: int) -> UserInfo:
        try:
            resp = httpx.get(f"{USER_SERVICE_URL}/users/{user_id}", timeout=5.0)
            resp.raise_for_status()
            return UserInfo(**resp.json())
        except Exception:
            raise HTTPException(status_code=503, detail="User service unavailable")

    def create_booking(self, payload: BookingCreate) -> BookingOut:
        provider = get_provider(payload.provider_id)
        user = upsert_user(name=payload.name, email=payload.email)

        try:
            scheduled_at = datetime.fromisoformat(payload.scheduled_at)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid scheduled_at format. Use ISO 8601.")

        booking = self.repo.create(
            user_id=user.id,
            provider_id=provider.id,
            scheduled_at=scheduled_at,
        )
        self.db.commit()
        self.db.refresh(booking)

        send_booking_confirmation(
            to_email=user.email,
            to_name=user.name or user.email,
            provider_name=provider.name,
            service_name=provider.service.name,
            scheduled_at=scheduled_at.strftime("%A, %d %B %Y at %I:%M %p"),
            booking_id=booking.id,
        )

        return BookingOut(
            id=booking.id,
            scheduled_at=booking.scheduled_at,
            status=booking.status,
            user=user,
            provider=provider,
        )

    def list_bookings(self) -> list[BookingOut]:
        bookings = self.repo.list_all()
        result = []
        for b in bookings:
            try:
                provider = get_provider(b.provider_id)
                user = self._fetch_user(b.user_id)
                result.append(BookingOut(
                    id=b.id,
                    scheduled_at=b.scheduled_at,
                    status=b.status,
                    user=user,
                    provider=provider,
                ))
            except Exception:
                continue
        return result
