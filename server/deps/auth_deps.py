from typing import Any, Optional

from fastapi import Depends, Request, Response, HTTPException
from authx.main import AuthX

from server.core.config import settings
from server.core.jwt_service import JWTService
from server.core.jwt_config import AuthX
from authx import exceptions as authx_exceptions
from server.core.jwt_config import auth
from server.core.logging_config import logger
from jose import JWTError, jwt

auth: AuthX
jwt_service = JWTService()

from fastapi import Request, Response, HTTPException, Depends

async def get_current_user(
    request: Request, response: Response,
):
    try:
        access_token = await auth.get_access_token_from_request(request)

        payload = auth.verify_token(access_token, verify_csrf=False)

        payload_dict = dict(payload)
        logger.debug(payload_dict)

        # if payload.type != "access":
        #     raise Exception("Not an access token")

        return {"valid": True, "user_id": payload.sub, "payload": payload}

    except Exception as e:
        return {"valid": False, "error": str(e)}
