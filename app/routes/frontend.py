from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "index.html"


@router.get("/ui", response_class=FileResponse)
def get_frontend():
    return FileResponse(
        path=TEMPLATE_PATH,
        media_type="text/html",
    )
