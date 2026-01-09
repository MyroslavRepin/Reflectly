from fastapi import Depends, Request, Response, HTTPException
from authx.main import AuthX
from server.core.jwt_service import JWTService
from server.core.config import settings
from server.core.jwt_config import AuthX

auth: AuthX
jwt_service = JWTService()

async def get_current_user(request: Request, response: Response):
    # Попытка получить user_id из access токена
    try:
        payload = await auth.access_token_required(request)
        user_id = payload["sub"]
        return user_id
    except Exception:
        # Если access просрочен — пробуем refresh
        try:
            refresh_payload = await auth.refresh_token_required(request)
            user_id = refresh_payload["sub"]

            # Создаём новый access и ставим в cookie
            new_access = jwt_service.create_access_token(user_id)
            response.set_cookie(
                key=settings.jwt_access_cookie_name,
                value=new_access,
                httponly=True,
                samesite="lax",
            )

            return user_id
        except Exception:
            raise HTTPException(status_code=401, detail="Authentication failed")

