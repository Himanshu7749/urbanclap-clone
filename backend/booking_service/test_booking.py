import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient

MOCK_USER = {"id": 1, "name": "Test User", "email": "test@example.com"}
MOCK_PROVIDER = {
    "id": 1,
    "name": "Alice the Barber",
    "rating": 4.8,
    "service": {"id": 1, "name": "Barber", "slug": "barber"},
}

# Patch external HTTP calls for the entire test session
@pytest.fixture(autouse=True, scope="session")
def mock_external():
    with patch("clients.upsert_user", return_value=MagicMock(**MOCK_USER)) as mu, \
         patch("clients.get_provider", return_value=MagicMock(**MOCK_PROVIDER)) as mp, \
         patch("clients.send_booking_confirmation", return_value=None) as mn:
        # Make the mocks behave like the schema objects
        mu.return_value.id = 1
        mu.return_value.name = "Test User"
        mu.return_value.email = "test@example.com"
        mp.return_value.id = 1
        mp.return_value.name = "Alice the Barber"
        mp.return_value.rating = 4.8
        mp.return_value.service = MagicMock(id=1, name="Barber", slug="barber")
        yield


from main import app
client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_booking():
    r = client.post("/bookings", json={
        "provider_id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "scheduled_at": "2026-12-01T10:00:00",
    })
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "pending"
    assert body["id"] is not None


def test_create_booking_invalid_date():
    r = client.post("/bookings", json={
        "provider_id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "scheduled_at": "not-a-date",
    })
    assert r.status_code == 400


def test_list_bookings():
    # create one first
    client.post("/bookings", json={
        "provider_id": 1,
        "name": "List User",
        "email": "list@example.com",
        "scheduled_at": "2026-12-02T11:00:00",
    })
    r = client.get("/bookings")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
