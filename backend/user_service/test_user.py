import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Override engine before app imports anything else
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

from main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_register():
    r = client.post("/auth/register", json={
        "name": "Alice", "email": "alice@test.com", "password": "secret123",
    })
    assert r.status_code == 201
    body = r.json()
    assert "access_token" in body
    assert body["user"]["email"] == "alice@test.com"


def test_register_duplicate_email():
    payload = {"name": "Bob", "email": "bob@test.com", "password": "secret"}
    client.post("/auth/register", json=payload)
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 409


def test_login_success():
    client.post("/auth/register", json={
        "name": "Carol", "email": "carol@test.com", "password": "pass123",
    })
    r = client.post("/auth/login", json={"email": "carol@test.com", "password": "pass123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password():
    client.post("/auth/register", json={
        "name": "Dave", "email": "dave@test.com", "password": "correct",
    })
    r = client.post("/auth/login", json={"email": "dave@test.com", "password": "wrong"})
    assert r.status_code == 401


def test_me_authenticated():
    reg = client.post("/auth/register", json={
        "name": "Eve", "email": "eve@test.com", "password": "pw12345",
    })
    token = reg.json()["access_token"]
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == "eve@test.com"


def test_me_no_token():
    r = client.get("/auth/me")
    assert r.status_code == 401


def test_upsert_creates_user():
    r = client.post("/users/upsert", json={"name": "Frank", "email": "frank@test.com"})
    assert r.status_code == 201
    assert r.json()["email"] == "frank@test.com"


def test_upsert_updates_existing():
    client.post("/users/upsert", json={"name": "Grace", "email": "grace@test.com"})
    r = client.post("/users/upsert", json={"name": "Grace Updated", "email": "grace@test.com"})
    assert r.status_code == 201
    assert r.json()["name"] == "Grace Updated"
