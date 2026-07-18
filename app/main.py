from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import logger


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
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
