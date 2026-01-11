import os

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.exceptions import HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.config import settings
from server.core.jwt_config import auth
from server.core.jwt_service import JWTService
from server.db.repositories.entries import TimeEntriesRepository
from server.db.sessions import get_db
from server.deps.auth_deps import get_current_user
from server.deps.schemas.entries_schemas import EntryCreate
from server.deps.schemas.users_schemes import UserCreate, UserLogin
from server.core.logging_config import logger
from sqlalchemy import select
router = APIRouter()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(
    BASE_DIR, "..", "..", "..", "frontend"))

templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates/routes"))

entries_repo = TimeEntriesRepository()

@router.post("/api/v1/timer/start")
async def start_timer(
    jwt_decoded: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = jwt_decoded["user_id"]

    new_entry = EntryCreate(user_id=user_id)
    try:
        # Todo: if entry without end_time is existin return error
        stmt = select(entries_repo.model).where(
            entries_repo.model.user_id == int(user_id),
            entries_repo.model.ended_at.is_(None)
        )
        result = await db.execute(stmt)
        running_entry = result.scalars().first()

        if running_entry:
            return {"error": "Timer is already running"}

        return await entries_repo.create(db, new_entry=new_entry)

    except Exception as e:
        logger.error(f"Error creating entry for user {user_id}: {e}")
        return {"error": str(e)}

@router.post("/api/v1/timer/stop")
async def stop_timer(
        user_id: str = Depends(get_current_user),
):
    return user_id