import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

USER_SERVICE    = "http://localhost:8001"
CATALOG_SERVICE = "http://localhost:8002"
BOOKING_SERVICE = "http://localhost:8003"

# Maps gateway path prefix -> upstream base URL
ROUTES: dict[str, str] = {
    "/api/users":     USER_SERVICE,
    "/api/services":  CATALOG_SERVICE,
    "/api/providers": CATALOG_SERVICE,
    "/api/bookings":  BOOKING_SERVICE,
}


def _resolve(path: str) -> str | None:
    for prefix, upstream in ROUTES.items():
        if path.startswith(prefix):
            # Strip /api prefix, keep the rest
            stripped = path[len("/api"):]
            return upstream + stripped
    return None


@app.api_route(
    "/api/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def gateway(path: str, request: Request):
    full_path = f"/api/{path}"
    upstream_url = _resolve(full_path)

    if upstream_url is None:
        return Response(content="Route not found", status_code=404)

    body = await request.body()
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ("host", "content-length")
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        upstream_resp = await client.request(
            method=request.method,
            url=upstream_url,
            params=request.query_params,
            headers=headers,
            content=body,
        )

    return Response(
        content=upstream_resp.content,
        status_code=upstream_resp.status_code,
        headers=dict(upstream_resp.headers),
        media_type=upstream_resp.headers.get("content-type"),
    )


@app.get("/health")
async def health():
    results = {}
    services = {
        "user":    f"{USER_SERVICE}/health",
        "catalog": f"{CATALOG_SERVICE}/health",
        "booking": f"{BOOKING_SERVICE}/health",
    }
    async with httpx.AsyncClient(timeout=3.0) as client:
        for name, url in services.items():
            try:
                r = await client.get(url)
                results[name] = "ok" if r.status_code == 200 else "degraded"
            except Exception:
                results[name] = "unreachable"
    overall = "ok" if all(v == "ok" for v in results.values()) else "degraded"
    return {"status": overall, "services": results}
