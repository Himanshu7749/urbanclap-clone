from sqlalchemy.orm import Session
from models import Service, Provider


class CatalogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_service_by_slug(self, slug: str) -> Service | None:
        return self.db.query(Service).filter(Service.slug == slug).first()

    def get_provider_by_id(self, provider_id: int) -> Provider | None:
        return self.db.query(Provider).filter(Provider.id == provider_id).first()

    def list_services(self) -> list[Service]:
        return self.db.query(Service).all()

    def upsert_service(self, name: str, slug: str) -> Service:
        svc = self.db.query(Service).filter(Service.slug == slug).first()
        if not svc:
            svc = Service(name=name, slug=slug)
            self.db.add(svc)
            self.db.flush()
        return svc

    def upsert_provider(self, name: str, rating: float, service_id: int) -> Provider:
        p = self.db.query(Provider).filter(Provider.name == name).first()
        if p:
            p.rating = rating
            p.service_id = service_id
        else:
            p = Provider(name=name, rating=rating, service_id=service_id)
            self.db.add(p)
            self.db.flush()
        return p
