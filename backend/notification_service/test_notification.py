from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_booking_confirmation_sends_email():
    with patch("main.send_booking_confirmation", return_value=None) as mock_send:
        r = client.post("/notify/booking-confirmation", json={
            "to_email": "user@example.com",
            "to_name": "Test User",
            "provider_name": "Alice the Barber",
            "service_name": "Barber",
            "scheduled_at": "Monday, 01 December 2026 at 10:00 AM",
            "booking_id": 42,
        })
        assert r.status_code == 200
        assert r.json()["sent"] is True
        mock_send.assert_called_once()


def test_booking_confirmation_smtp_failure():
    with patch("main.send_booking_confirmation", side_effect=Exception("SMTP down")):
        r = client.post("/notify/booking-confirmation", json={
            "to_email": "user@example.com",
            "to_name": "Test User",
            "provider_name": "Bob the Plumber",
            "service_name": "Plumbing",
            "scheduled_at": "Tuesday, 02 December 2026 at 11:00 AM",
            "booking_id": 43,
        })
        assert r.status_code == 500
        assert "SMTP down" in r.json()["detail"]
