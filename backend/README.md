# UrbanServe — Python Microservices Backend

## Architecture

```
Next.js (:3000)
      |
  API Gateway (:8000)          ← single entry point, handles CORS
      |
  ┌───┴──────────────────────┐
  │          │               │
User Svc  Catalog Svc   Booking Svc
(:8001)    (:8002)       (:8003)
users.db  catalog.db   bookings.db
```

Each service is fully independent with its own database, models, repository, and service layer.
The Booking Service calls User + Catalog via HTTP through `clients.py`.

## Services

| Service | Port | Database | Responsibilities |
|---|---|---|---|
| API Gateway | 8000 | — | Route forwarding, CORS, health aggregation |
| User Service | 8001 | users.db | Create/get/upsert users by email |
| Catalog Service | 8002 | catalog.db | Services and providers, auto-seeded on startup |
| Booking Service | 8003 | bookings.db | Create bookings, list bookings with enriched data |

## Layers (per service)

```
main.py        ← FastAPI routes (HTTP layer)
service.py     ← Business logic
repository.py  ← Database queries (SQLAlchemy)
models.py      ← ORM table definitions
schemas.py     ← Pydantic request/response models
database.py    ← Engine + session factory
clients.py     ← HTTP calls to other services (Booking only)
```

## API Endpoints (via Gateway)

| Method | Path | Description |
|---|---|---|
| GET | /health | Health check for all services |
| GET | /api/services | List all service categories |
| GET | /api/services/{slug} | Get service with providers |
| GET | /api/providers/{id} | Get provider with service info |
| GET | /api/users | List all users |
| GET | /api/users/{id} | Get user by ID |
| POST | /api/users/upsert | Create or update user by email |
| GET | /api/bookings | List all bookings (enriched) |
| POST | /api/bookings | Create a booking |

## Running

### Install dependencies (once)
```bash
pip install -r requirements.txt
```

### Start all services (Windows)
```bat
start.bat
```

### Or start manually (one terminal each)
```bash
cd user_service    && python -m uvicorn main:app --port 8001 --reload
cd catalog_service && python -m uvicorn main:app --port 8002 --reload
cd booking_service && python -m uvicorn main:app --port 8003 --reload
cd gateway         && python -m uvicorn main:app --port 8000 --reload
```

### Then start Next.js
```bash
npm run dev
```

Interactive API docs available at each service:
- http://localhost:8000/docs (Gateway)
- http://localhost:8001/docs (User Service)
- http://localhost:8002/docs (Catalog Service)
- http://localhost:8003/docs (Booking Service)
