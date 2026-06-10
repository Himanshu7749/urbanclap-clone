from fastapi import FastAPI, HTTPException
from schemas import BookingConfirmationRequest
from mailer import send_booking_confirmation

app = FastAPI(title="Notification Service", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "notification"}


@app.post("/notify/booking-confirmation", status_code=200)
def booking_confirmation(payload: BookingConfirmationRequest):
    try:
        send_booking_confirmation(
            to_email=payload.to_email,
            to_name=payload.to_name,
            provider_name=payload.provider_name,
            service_name=payload.service_name,
            scheduled_at=payload.scheduled_at,
            booking_id=payload.booking_id,
        )
        return {"sent": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email failed: {str(e)}")
