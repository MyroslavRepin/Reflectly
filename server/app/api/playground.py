from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
from server.core.config import settings
from server.db.sessions import get_db
from sqlalchemy import text, select

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]


FRONTEND_DIR = PROJECT_ROOT / "frontend"

templates = Jinja2Templates(
    directory=FRONTEND_DIR / "templates/routes"
)

@router.get("/playground")
async def landing(request: Request, db: AsyncSession = Depends(get_db)):
    stmt = select(1)
    result = await db.execute(stmt)
    return result.scalars().first()
    # return settings.db_name