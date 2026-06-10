import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

import database
_test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
database.engine = _test_engine
database.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)

from models import Base
Base.metadata.create_all(bind=_test_engine)

from schemas import UserInfo, ProviderInfo, ServiceInfo

MOCK_SERVICE  = ServiceInfo(id=1, name="Barber", slug="barber")
MOCK_PROVIDER = ProviderInfo(id=1, name="Alice the Barber", rating=4.8, service=MOCK_SERVICE)
MOCK_USER     = UserInfo(id=1, name="Test User", email="test@example.com")

from main import app
client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_booking():
    with patch("service.upsert_user", return_value=MOCK_USER), \
         patch("service.get_provider", return_value=MOCK_PROVIDER), \
         patch("service.send_booking_confirmation", return_value=None):
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
    with patch("service.upsert_user", return_value=MOCK_USER), \
         patch("service.get_provider", return_value=MOCK_PROVIDER), \
         patch("service.send_booking_confirmation", return_value=None):
        r = client.post("/bookings", json={
            "provider_id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "scheduled_at": "not-a-date",
        })
    assert r.status_code == 400


def test_list_bookings():
    with patch("service.upsert_user", return_value=MOCK_USER), \
         patch("service.get_provider", return_value=MOCK_PROVIDER), \
         patch("service.send_booking_confirmation", return_value=None), \
         patch("service.BookingService._fetch_user", return_value=MOCK_USER):
        client.post("/bookings", json={
            "provider_id": 1,
            "name": "List User",
            "email": "list@example.com",
            "scheduled_at": "2026-12-02T11:00:00",
        })
        r = client.get("/bookings")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1
