from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
import models  # noqa: F401
from service import CatalogService
from schemas import ServiceOut, ServiceWithProviders, ProviderOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catalog Service", version="1.0.0")


def get_service(db: Session = Depends(get_db)) -> CatalogService:
    return CatalogService(db)


@app.on_event("startup")
def seed_on_startup():
    db = next(get_db())
    CatalogService(db).seed()


@app.get("/health")
def health():
    return {"status": "ok", "service": "catalog"}


@app.get("/services", response_model=list[ServiceOut])
def list_services(svc: CatalogService = Depends(get_service)):
    return svc.list_services()


@app.get("/services/{slug}", response_model=ServiceWithProviders)
def get_service_by_slug(slug: str, svc: CatalogService = Depends(get_service)):
    return svc.get_service_by_slug(slug)


@app.get("/providers/{provider_id}", response_model=ProviderOut)
def get_provider(provider_id: int, svc: CatalogService = Depends(get_service)):
    return svc.get_provider(provider_id)
