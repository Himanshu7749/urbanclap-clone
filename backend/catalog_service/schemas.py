from pydantic import BaseModel
from typing import Optional


class ServiceOut(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}


class ProviderOut(BaseModel):
    id: int
    name: str
    rating: Optional[float]
    service: ServiceOut

    model_config = {"from_attributes": True}


class ServiceWithProviders(ServiceOut):
    providers: list[ProviderOut]
