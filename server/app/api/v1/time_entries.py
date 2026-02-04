import datetime
import os

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.exceptions import HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from server.core.config import settings
from server.core.jwt_config import auth
from server.core.jwt_service import JWTService
from server.db.repositories.entries import TimeEntriesRepository
from server.db.sessions import get_db
from server.deps.auth_deps import get_current_user
from server.deps.schemas.entries_schemas import EntryCreate
from server.core.logging_config import logger
from sqlalchemy import select
router = APIRouter()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(
    BASE_DIR, "..", "..", "..", "frontend"))

templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates/routes"))

entries_repo = TimeEntriesRepository()

@router.post("/api/v1/time-entries/start")
async def start_timer(
    jwt_decoded: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = jwt_decoded["user_id"]

    new_entry = EntryCreate(user_id=user_id)
    try:
        stmt = select(entries_repo.model).where(
            entries_repo.model.user_id == int(user_id),
            entries_repo.model.ended_at.is_(None)
        )
        result = await db.execute(stmt)
        running_entry = result.scalars().first()

        if running_entry:
            logger.warning(f"User {user_id} already has running entry")
            raise HTTPException(status_code=409, detail="Timer is already running")

        created_entry = await entries_repo.create(db, new_entry=new_entry)
        return {
            "id": created_entry.id,
            "started_at": created_entry.started_at,
            "user_id": created_entry.user_id
        }

    except HTTPException:
        # Пробрасываем HTTPException как есть, не логируем как 500
        raise

    except Exception as e:
        logger.error(f"Error creating entry for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/api/v1/time-entries/stop")
async def stop_timer(
        jwt_decoded: str = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    user_id = jwt_decoded["user_id"]
    stmt = select(entries_repo.model).where(
        entries_repo.model.user_id == int(user_id),
        entries_repo.model.ended_at.is_(None)
    )
    result = await db.execute(stmt)
    running_entry = result.scalars().first()
    if not running_entry:
        raise HTTPException(status_code=404, detail="No running timer found")
    running_entry.ended_at = datetime.datetime.now(datetime.timezone.utc)
    try:
        await db.commit()
        await db.refresh(running_entry)
        data = {
            "id": running_entry.id,
            "started_at": running_entry.started_at,
            "ended_at": running_entry.ended_at
        }
        return data

    except Exception as e:
        logger.error(f"Error stopping timer for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error stopping timer")

@router.get("/api/v1/time-entries/current-running")
async def get_current_timer(
        jwt_decoded: str = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    user_id = jwt_decoded["user_id"]

    stmt = select(entries_repo.model).where(
        entries_repo.model.user_id == int(user_id),
        entries_repo.model.ended_at.is_(None)
    )
    result = await db.execute(stmt)
    running_entry = result.scalars().first()
    if not running_entry:
        return None
    data = {
        "id": running_entry.id,
        "started_at": running_entry.started_at,
    }
    return data

@router.post("/api/v1/time-entries/pause")
async def pause_timer(jwt_decoded: str = Depends(get_current_user)):
    return "pause"

@router.get('/api/v1/time-entries')
async def get_all_sessions(jwt_decoded: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_id = jwt_decoded["user_id"]
    try:
        stmt = select(entries_repo.model).where(entries_repo.model.user_id == int(user_id))
        result = await db.execute(stmt)
        entries = result.scalars().all()
        logger.debug(f"Found {len(entries)} entries for user {user_id}")
        return entries if entries else []
    except Exception as e:
        logger.error(f"Error getting entries for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error getting entries")

@router.get('/api/v1/time-entries/{entry_id}')
async def get_timer_by_id(entry_id: int, jwt_decoded: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_id = jwt_decoded["user_id"]
    try:
        stmt = select(entries_repo.model).where(entries_repo.model.id == entry_id, entries_repo.model.user_id == int(user_id))
        result = await db.execute(stmt)
        entry = result.scalars().first()
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return entry
    except Exception as e:
        logger.error(f"Error getting entry {entry_id} for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error getting entry")