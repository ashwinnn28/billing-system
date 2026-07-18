from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import logger
from app.api.v1.router import api_router
from app.api.v1.endpoints import admin
from app.routes import frontend
from app.utils.create_admin import create_admin_user

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


# API Version 1 Routes
app.include_router(
    api_router,
    prefix="/api/v1"
)

# Admin Routes
app.include_router(
    admin.router,
    prefix="/admin"
)

# Frontend UI
app.include_router(
    frontend.router
)

@app.on_event("startup")
async def startup():
    create_admin_user()
    logger.info("Billing System Started")


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "running",
        "application": settings.app_name,
        "version": settings.app_version,
    }
