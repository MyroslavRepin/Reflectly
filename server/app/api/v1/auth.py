from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from server.core.config import settings
from server.core.jwt_config import get_authx
from server.core.jwt_service import JWTService
from server.db.models.users import User
from server.db.sessions import get_db
from server.deps.schemas.users_schemes import UserCreate, UserLogin, SignupRequest
from server.utils.security.auth import hash_password
from server.db.repositories.users import UserRepository
from server.core.logging_config import logger
from passlib.hash import argon2


router = APIRouter()

jwt_service = JWTService()

@router.post('/api/v1/auth/signup')
async def signup_api(
    response: Response,
    user_data: SignupRequest,
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository() # Repository to easily interact with the User model (db)

    try:
        user = UserCreate(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password)
        )
        created_user = await repo.create(db, **user.dict())
        logger.debug(f"User {user_data.username} created")
        data = {
          "ok": True,
          "user": {
            "id": created_user.id,
            "username": created_user.username,
            "email": created_user.email
          }
        }
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")

    access_token = jwt_service.create_access_token(user_id=created_user.id)
    refresh_token = jwt_service.create_refresh_token(user_id=created_user.id)

    try:
        jwt_service.set_cokies(
            access_token=access_token,
            refresh_token=refresh_token,
            response=response
        )
    except Exception as e:
        logger.error(f"Error setting cookies: {e}")
        raise HTTPException(
            status_code=500,
            detail="COOKIE_SET_FAILED"
        )

    return data # Returning the created user


@router.post("/api/v1/auth/login")
async def login_post(
        user_credentials: UserLogin,
        response: Response,
        db: AsyncSession = Depends(get_db),
    ):

    logger.info(user_credentials)

    stmt = select(User).where(
        or_(
            User.email == user_credentials.login,
            User.username == user_credentials.login
        )
    )
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password"
        )
    logger.info(f"user.hashed_password: {user.hashed_password}")
    logger.info(f"hashed_password (form): {user_credentials.password}")

    if not argon2.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password"
        )

    auth = get_authx()

    access_token = auth.create_access_token(uid=str(user.id))
    refresh_token = auth.create_refresh_token(uid=str(user.id))

    jwt_service.set_cokies(
        access_token=access_token,
        refresh_token=refresh_token,
        response=response
    )

    data = {
        "ok": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }
    return data


# Logout API
@router.post("/api/v1/auth/logout")
async def logout(response: Response):
    response.delete_cookie(
        key=settings.jwt_access_cookie_name,
        path="/",
        samesite="lax",
        secure=False,
    )
    response.delete_cookie(
        key=settings.jwt_refresh_cookie_name,
        path="/",
        samesite="lax",
        secure=False,
    )
    data = {
        "ok": True
    }
    return data
