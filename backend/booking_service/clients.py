import httpx
from schemas import UserInfo, ProviderInfo
from fastapi import HTTPException

USER_SERVICE_URL         = "http://localhost:8001"
CATALOG_SERVICE_URL      = "http://localhost:8002"
NOTIFICATION_SERVICE_URL = "http://localhost:8004"


def upsert_user(name: str, email: str) -> UserInfo:
    try:
        resp = httpx.post(
            f"{USER_SERVICE_URL}/users/upsert",
            json={"name": name, "email": email},
            timeout=5.0,
        )
        resp.raise_for_status()
        return UserInfo(**resp.json())
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="User service error")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="User service unavailable")


def get_provider(provider_id: int) -> ProviderInfo:
    try:
        resp = httpx.get(
            f"{CATALOG_SERVICE_URL}/providers/{provider_id}",
            timeout=5.0,
        )
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Provider not found")
        resp.raise_for_status()
        return ProviderInfo(**resp.json())
    except HTTPException:
        raise
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Catalog service unavailable")


def send_booking_confirmation(
    to_email: str,
    to_name: str,
    provider_name: str,
    service_name: str,
    scheduled_at: str,
    booking_id: int,
) -> None:
    # Fire-and-forget: log on failure but don't block the booking response
    try:
        httpx.post(
            f"{NOTIFICATION_SERVICE_URL}/notify/booking-confirmation",
            json={
                "to_email": to_email,
                "to_name": to_name,
                "provider_name": provider_name,
                "service_name": service_name,
                "scheduled_at": scheduled_at,
                "booking_id": booking_id,
            },
            timeout=5.0,
        )
    except Exception:
        pass  # notification failure must never fail the booking itself
