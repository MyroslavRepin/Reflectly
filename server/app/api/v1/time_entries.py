import datetime
import os

from dateutil.parser import isoparse
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
from server.db.models.entries import TimeEntry
from server.db.models.users import User
from server.db.repositories.entries import TimeEntriesRepository
from server.db.sessions import get_db
from server.deps.auth_deps import get_current_user
from server.deps.schemas.entries_schemas import EntryCreate, EntryStartRequest, EntryResponse, EntryUpdate
from server.core.logging_config import logger
from sqlalchemy import select

from server.utils.security.auth import hash_password

router = APIRouter()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(
    BASE_DIR, "..", "..", "..", "frontend"))

templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates/routes"))

entries_repo = TimeEntriesRepository()

@router.post("/api/v1/time-entries/start")
async def start_session(
    request: EntryStartRequest,
    jwt_decoded: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = jwt_decoded["user_id"]
    
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

        new_entry = EntryCreate(
            user_id=int(user_id),
            title=request.title,
            description=request.description
        )
        
        created_entry = await entries_repo.create(db, new_entry=new_entry)
        return {
            "id": created_entry.id,
            "started_at": created_entry.started_at,
            "user_id": created_entry.user_id
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error creating entry for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/api/v1/time-entries/stop")
async def stop_session(
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
async def get_current_sessiom(
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
async def pause_session(jwt_decoded: str = Depends(get_current_user)):
    return "this feature is not yet implemented"

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

@router.get('/api/v1/time-entries/{entry_id}', response_model=EntryResponse)
async def get_session(entry_id: int, jwt_decoded: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_id = jwt_decoded["user_id"]
    try:
        stmt = select(entries_repo.model).where(entries_repo.model.id == entry_id, entries_repo.model.user_id == int(user_id))
        try:
            result = await db.execute(stmt)
        except Exception as e:
            logger.error(f"Error getting entry {entry_id} for user {user_id}: {e}")
            HTTPException(status_code=500, detail="Error getting entry")

        entry = result.scalars().first()
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return entry
    except Exception as e:
        logger.error(f"Error getting entry {entry_id} for user {user_id}: {e}")
        raise HTTPException(status_code=403, detail="Forbidden to fetch this entry")

@router.patch('/api/v1/time-entries/{entry_id}', response_model=EntryResponse)
async def update_session(
        session_id: int,
        session_data: EntryUpdate,
        db: AsyncSession = Depends(get_db),
        jwt_decoded: str = Depends(get_current_user),
):
    user_id = int(jwt_decoded["user_id"])
    stmt = select(TimeEntry).where(TimeEntry.user_id == user_id, TimeEntry.id == session_id)
    result = await db.execute(stmt)
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    logger.debug(f"Updating session {session_id}")

    update_dict = session_data.model_dump(exclude_unset=True)

    # Convert ISO string datetime fields to datetime objects
    for key in ["started_at", "ended_at"]:
        if key in update_dict:
            # If value is None (null), keep it as None to clear the field
            if update_dict[key] is None:
                continue
            # Otherwise parse the ISO string to datetime
            update_dict[key] = isoparse(update_dict[key])

    try:
        updated_entry = await entries_repo.update(db, entry_id=session_id, **update_dict)
    except Exception as e:
        logger.error(f"Error updating entry {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating entry")

    return updated_entry

@router.delete('/api/v1/time-entries/{entry_id}')
async def delete_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    jwt_decoded: str = Depends(get_current_user),
):
    user_id = int(jwt_decoded["user_id"])
    stmt = select(TimeEntry).where(TimeEntry.user_id == user_id, TimeEntry.id == session_id)
    try:
        result = await db.execute(stmt)
    except Exception as e:
        logger.error(f"Error deleting entry {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Error getting entry")
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    try:
        await db.delete(entry)
        await db.commit()
    except Exception as e:
        logger.error(f"Error deleting entry {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting entry")
    logger.debug(f"Entry {session_id} deleted")
    return {"deleted": True, "id": session_id}
