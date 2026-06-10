import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# The startup event seeds the DB, but TestClient doesn't run lifespan events by default.
# Manually seed before tests.
@pytest.fixture(autouse=True, scope="session")
def seed_db():
    from database import get_db
    from service import CatalogService
    db = next(get_db())
    CatalogService(db).seed()


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_list_services():
    r = client.get("/services")
    assert r.status_code == 200
    slugs = [s["slug"] for s in r.json()]
    assert "barber" in slugs
    assert "plumbing" in slugs
    assert "cleaning" in slugs


def test_get_service_by_slug():
    r = client.get("/services/barber")
    assert r.status_code == 200
    data = r.json()
    assert data["slug"] == "barber"
    assert len(data["providers"]) > 0


def test_get_service_not_found():
    r = client.get("/services/nonexistent")
    assert r.status_code == 404


def test_get_provider():
    # get the first provider from barber service
    svc = client.get("/services/barber").json()
    provider_id = svc["providers"][0]["id"]
    r = client.get(f"/providers/{provider_id}")
    assert r.status_code == 200
    assert r.json()["service"]["slug"] == "barber"


def test_get_provider_not_found():
    r = client.get("/providers/99999")
    assert r.status_code == 404
