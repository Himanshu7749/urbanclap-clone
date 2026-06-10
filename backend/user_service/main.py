from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import User  # noqa: F401
from service import UserService
from schemas import UserCreate, UserRegister, UserLogin, UserOut, TokenOut
from auth import get_current_user_id

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service", version="2.0.0")


def get_svc(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@app.get("/health")
def health():
    return {"status": "ok", "service": "user"}


# --- Auth ---

@app.post("/auth/register", response_model=TokenOut, status_code=201)
def register(payload: UserRegister, svc: UserService = Depends(get_svc)):
    return svc.register(name=payload.name, email=payload.email, password=payload.password)


@app.post("/auth/login", response_model=TokenOut)
def login(payload: UserLogin, svc: UserService = Depends(get_svc)):
    return svc.login(email=payload.email, password=payload.password)


@app.get("/auth/me", response_model=UserOut)
def me(user_id: int = Depends(get_current_user_id), svc: UserService = Depends(get_svc)):
    return svc.get_user(user_id)


# --- Internal (called by other services) ---

@app.get("/users", response_model=list[UserOut])
def list_users(svc: UserService = Depends(get_svc)):
    return svc.list_users()


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, svc: UserService = Depends(get_svc)):
    return svc.get_user(user_id)


@app.post("/users/upsert", response_model=UserOut, status_code=201)
def upsert_user(payload: UserCreate, svc: UserService = Depends(get_svc)):
    return svc.upsert_user(name=payload.name, email=payload.email)
