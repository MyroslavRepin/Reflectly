from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
from server.core.config import settings
from server.core.jwt_service import JWTService
from server.db.sessions import get_db
from server.utils.security.auth import hash_password
from server.core.logging_config import logger
from sqlalchemy import text, select

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]


FRONTEND_DIR = PROJECT_ROOT / "frontend"

templates = Jinja2Templates(
    directory=FRONTEND_DIR / "templates/routes"
)

jwt_service = JWTService()

@router.get("/playground")
async def landing(request: Request, db: AsyncSession = Depends(get_db)):
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwianRpIjoiOWEwNjA4NjEtMmUwMy00ODFlLWFhODUtN2FhNTcyMDNmOTgzIiwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZSwiY3NyZiI6IiIsImlhdCI6MTc2NzkwODk3OSwiZXhwIjoxNzY3OTA5MDA5LjI5MjUxN30.sjcxXYs3NuiAwBtsflE6UBW2oSLbGJ9ulHS1hfN9ge0"
    return jwt_service.decode_token(access_token)