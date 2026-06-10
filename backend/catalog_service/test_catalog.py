import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

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

# Seed test data directly before importing app
from models import Service, Provider
from database import SessionLocal as TestSession

def _seed():
    db = TestSession()
    if db.query(Service).count() > 0:
        db.close()
        return
    services = [
        Service(name="Barber", slug="barber"),
        Service(name="Plumbing", slug="plumbing"),
        Service(name="Cleaning", slug="cleaning"),
    ]
    db.add_all(services)
    db.commit()
    barber = db.query(Service).filter_by(slug="barber").first()
    plumbing = db.query(Service).filter_by(slug="plumbing").first()
    db.add_all([
        Provider(name="Alice the Barber", rating=4.8, service_id=barber.id),
        Provider(name="Bob the Barber", rating=4.6, service_id=barber.id),
        Provider(name="Cathy the Plumber", rating=4.7, service_id=plumbing.id),
    ])
    db.commit()
    db.close()

_seed()

from main import app

client = TestClient(app)


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
    svc = client.get("/services/barber").json()
    provider_id = svc["providers"][0]["id"]
    r = client.get(f"/providers/{provider_id}")
    assert r.status_code == 200
    assert r.json()["service"]["slug"] == "barber"


def test_get_provider_not_found():
    r = client.get("/providers/99999")
    assert r.status_code == 404
