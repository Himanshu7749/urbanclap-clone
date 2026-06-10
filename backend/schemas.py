from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ServiceBase(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}


class ProviderBase(BaseModel):
    id: int
    name: str
    rating: Optional[float]

    model_config = {"from_attributes": True}


class ServiceWithProviders(ServiceBase):
    providers: list[ProviderBase]


class ProviderWithService(ProviderBase):
    service: ServiceBase


class UserOut(BaseModel):
    id: int
    name: Optional[str]
    email: str

    model_config = {"from_attributes": True}


class ProviderInBooking(BaseModel):
    id: int
    name: str
    service: ServiceBase

    model_config = {"from_attributes": True}


class BookingOut(BaseModel):
    id: int
    scheduled_at: datetime
    status: str
    user: UserOut
    provider: ProviderInBooking

    model_config = {"from_attributes": True}


class BookingCreate(BaseModel):
    provider_id: int
    name: str
    email: str
    scheduled_at: str
