from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: Optional[str] = None
    email: str


class UserUpdate(BaseModel):
    name: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: Optional[str]
    email: str

    model_config = {"from_attributes": True}
