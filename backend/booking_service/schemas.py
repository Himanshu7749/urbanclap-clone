from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ServiceInfo(BaseModel):
    id: int
    name: str
    slug: str


class ProviderInfo(BaseModel):
    id: int
    name: str
    rating: Optional[float]
    service: ServiceInfo


class UserInfo(BaseModel):
    id: int
    name: Optional[str]
    email: str


class BookingCreate(BaseModel):
    provider_id: int
    name: str
    email: str
    scheduled_at: str


class BookingOut(BaseModel):
    id: int
    scheduled_at: datetime
    status: str
    user: UserInfo
    provider: ProviderInfo

    model_config = {"from_attributes": True}
