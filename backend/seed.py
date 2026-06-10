from database import engine, SessionLocal
from models import Base, Service, Provider

Base.metadata.create_all(bind=engine)

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


def seed():
    db = SessionLocal()
    try:
        for s in SERVICES:
            existing = db.query(Service).filter(Service.slug == s["slug"]).first()
            if not existing:
                db.add(Service(**s))
        db.commit()

        for p in PROVIDERS:
            service = db.query(Service).filter(Service.slug == p["service_slug"]).first()
            existing = db.query(Provider).filter(Provider.name == p["name"]).first()
            if existing:
                existing.rating = p["rating"]
                existing.service_id = service.id
            else:
                db.add(Provider(name=p["name"], rating=p["rating"], service_id=service.id))
        db.commit()
        print("Seed complete")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
