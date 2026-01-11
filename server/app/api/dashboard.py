import os

from fastapi import APIRouter, Request, Depends, Form
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


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(
    BASE_DIR, "..", "..", "..", "frontend"))

templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates/routes"))

jwt_service = JWTService()

@router.get("/dashboard")
async def dashboard(
    user_id: str = Depends(get_current_user),
):
    return user_id
    # try:
    #     access_token = await auth.get_access_token_from_request(request)
    #
    #     payload = auth.verify_token(access_token, verify_csrf=False)
    #     payload_dict = dict(payload)
    #     logger.debug(payload_dict)
    #
    #     # if payload.type != "access":
    #     #     raise Exception("Not an access token")
    #
    #     return {"valid": True, "user_id": payload.sub, "payload": payload}
    #
    # except Exception as e:
    #     return {"valid": False, "error": str(e)}