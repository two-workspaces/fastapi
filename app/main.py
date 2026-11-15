import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings, warnings
from app.log_config import setup_logging
from app.routers import items

setup_logging(settings.log_level)
log = logging.getLogger("app")
for problem in warnings:
    log.warning(problem)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Open database pools or clients here. Keep startup free of calls that can
    # fail (a database that isn't up yet): a crash here fails the deploy.
    log.info("starting", extra={"environment": settings.environment, "commit": settings.commit})
    yield
    log.info("stopping")


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
    docs_url="/docs" if settings.docs_enabled else None,
    redoc_url="/redoc" if settings.docs_enabled else None,
    openapi_url="/openapi.json" if settings.docs_enabled else None,
)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials="*" not in settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    if request.url.path != "/health":
        log.info(
            "%s %s %s",
            request.method,
            request.url.path,
            response.status_code,
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "ms": round((time.perf_counter() - start) * 1000, 1),
            },
        )
    return response


@app.get("/", tags=["meta"])
async def root() -> dict:
    return {
        "message": f"{settings.app_name} is running",
        "docs": "/docs" if settings.docs_enabled else None,
        "health": "/health",
    }


@app.get("/health", tags=["meta"])
async def health() -> dict:
    """Railway's healthcheck. Keep it fast and free of external calls."""
    return {"status": "ok", "environment": settings.environment, "commit": settings.commit or None}


app.include_router(items.router)
