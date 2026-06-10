from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import User  # noqa: F401 — ensures table is registered before create_all
from service import UserService
from schemas import UserCreate, UserOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service", version="1.0.0")


def get_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@app.get("/health")
def health():
    return {"status": "ok", "service": "user"}


@app.get("/users", response_model=list[UserOut])
def list_users(svc: UserService = Depends(get_service)):
    return svc.list_users()


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, svc: UserService = Depends(get_service)):
    return svc.get_user(user_id)


@app.post("/users/upsert", response_model=UserOut, status_code=201)
def upsert_user(payload: UserCreate, svc: UserService = Depends(get_service)):
    return svc.upsert_user(name=payload.name, email=payload.email)
