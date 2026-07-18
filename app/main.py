from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import logger
from app.api.v1.router import api_router


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


@app.on_event("startup")
async def startup():
    logger.info("Billing System Started")


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "running",
        "application": settings.app_name,
        "version": settings.app_version,
    }