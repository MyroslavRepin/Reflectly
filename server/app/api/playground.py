from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from pathlib import Path
from server.core.config import settings

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]


FRONTEND_DIR = PROJECT_ROOT / "frontend"

templates = Jinja2Templates(
    directory=FRONTEND_DIR / "templates/routes"
)

@router.get("/playground")
async def landing(request: Request):
    return settings.db_name