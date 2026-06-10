from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    name: Optional[str] = None
    email: str


class UserRegister(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: Optional[str]
    email: str

    model_config = {"from_attributes": True}


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
