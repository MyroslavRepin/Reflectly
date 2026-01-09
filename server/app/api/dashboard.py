import os

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response


from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from server.core.config import settings
from server.core.jwt_config import auth
from server.core.jwt_service import JWTService
from server.db.models.users import User
from server.db.sessions import get_db
from server.deps.auth_deps import get_current_user
from server.deps.schemas.users_schemes import UserCreate, UserLogin
from server.utils.security.auth import hash_password
from server.db.repositories.users import UserRepository
from server.core.logging_config import logger

router = APIRouter()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(
    BASE_DIR, "..", "..", "..", "frontend"))

templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates/routes"))

jwt_service = JWTService()

@router.get("/dashboard")
async def dashboard(
    user_id: str = Depends(get_current_user)
):
    return user_id
