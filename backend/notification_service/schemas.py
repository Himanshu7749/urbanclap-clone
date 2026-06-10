from pydantic import BaseModel


class BookingConfirmationRequest(BaseModel):
    to_email: str
    to_name: str
    provider_name: str
    service_name: str
    scheduled_at: str
    booking_id: int
