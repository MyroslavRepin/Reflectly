import os

from fastapi import APIRouter, Request, Depends, Form
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.exceptions import HTTPException

from server.core.config import settings
from server.core.jwt_config import auth
from server.core.jwt_service import JWTService
from server.db.sessions import get_db
from server.deps.auth_deps import get_current_user
from server.deps.schemas.users_schemes import UserCreate, UserLogin
from server.core.logging_config import logger

router = APIRouter()


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DIST_DIR = PROJECT_ROOT / "frontend" / "dist"

templates = Jinja2Templates(directory=str(DIST_DIR))


jwt_service = JWTService()

@router.get("/dashboard")
async def dashboard(
    request: Request,
    user_id: str = Depends(get_current_user),
):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
