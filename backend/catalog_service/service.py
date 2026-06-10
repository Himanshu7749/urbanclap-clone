from sqlalchemy.orm import Session
from repository import CatalogRepository
from schemas import ServiceOut, ServiceWithProviders, ProviderOut
from fastapi import HTTPException


class CatalogService:
    def __init__(self, db: Session):
        self.repo = CatalogRepository(db)
        self.db = db

    def get_service_by_slug(self, slug: str) -> ServiceWithProviders:
        svc = self.repo.get_service_by_slug(slug)
        if not svc:
            raise HTTPException(status_code=404, detail="Service not found")
        return ServiceWithProviders.model_validate(svc)

    def get_provider(self, provider_id: int) -> ProviderOut:
        p = self.repo.get_provider_by_id(provider_id)
        if not p:
            raise HTTPException(status_code=404, detail="Provider not found")
        return ProviderOut.model_validate(p)

    def list_services(self) -> list[ServiceOut]:
        return [ServiceOut.model_validate(s) for s in self.repo.list_services()]

    def seed(self):
        SERVICES = [
            {"name": "Barber", "slug": "barber"},
            {"name": "Plumbing", "slug": "plumbing"},
            {"name": "Cleaning", "slug": "cleaning"},
        ]
        PROVIDERS = [
            {"name": "Alice the Barber", "rating": 4.8, "service_slug": "barber"},
            {"name": "Bob the Barber", "rating": 4.6, "service_slug": "barber"},
            {"name": "Cathy the Plumber", "rating": 4.7, "service_slug": "plumbing"},
            {"name": "Dinesh the Plumber", "rating": 4.4, "service_slug": "plumbing"},
            {"name": "Ella the Cleaner", "rating": 4.9, "service_slug": "cleaning"},
            {"name": "Faisal the Cleaner", "rating": 4.5, "service_slug": "cleaning"},
        ]
        for s in SERVICES:
            self.repo.upsert_service(s["name"], s["slug"])
        self.db.commit()
        for p in PROVIDERS:
            svc = self.repo.get_service_by_slug(p["service_slug"])
            self.repo.upsert_provider(p["name"], p["rating"], svc.id)
        self.db.commit()
