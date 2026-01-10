import os
from os import name

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi import HTTPException, status


from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from server.core.config import settings
# from server.core.jwt_config import auth
from server.core.jwt_config import get_authx
from server.core.jwt_service import JWTService
from server.db.models.users import User
from server.db.sessions import get_db
from server.deps.schemas.users_schemes import UserCreate, UserLogin
from server.utils.security.auth import hash_password
from server.db.repositories.users import UserRepository
from server.core.logging_config import logger
from passlib.hash import argon2


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(
    BASE_DIR, "..", "..", "..", "frontend"))

templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates/routes"))

router = APIRouter()

jwt_service = JWTService()

# Signup API
@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    error = request.query_params.get("error")
    return templates.TemplateResponse("brutalist-signup.html", {"request": request, "error": error})


@router.post('/signup')
async def signup_post(
    response: Response,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    if password != confirm_password:
        return RedirectResponse("/signup?error=Passwords+do+not+match!&username=" + username + "&email=" + email, status_code=303)
    repo = UserRepository()

    try:
        user = UserCreate(
            username=username,
            email=email,
            hashed_password=hash_password(password)
        )
        await repo.create(db, **user.dict())
        logger.debug(f"User {username} created")

        try:
            response = RedirectResponse('/login', status_code=303)
        except Exception as e:
            logger.error(f"Error setting response: {e}")

        access_token = jwt_service.create_access_token(user_id=1)
        refresh_token = jwt_service.create_refresh_token(user_id=1)

        try:
            jwt_service.set_cokies(
                access_token=access_token,
                refresh_token=refresh_token,
                response=response
            )
        except Exception as e:
            logger.error(f"Error setting cookies: {e}")
            return RedirectResponse(f"/signup?error=Cookie+error&username={username}&email={email}", status_code=303)
        return response

    except IntegrityError:
        return RedirectResponse(f"/signup?error=Email+or+username+already+exists!&username={username}&email={email}",
                                status_code=303)
    except ValueError as e:
        return RedirectResponse(f"/signup?error={str(e)}&username={username}&email={email}", status_code=303)

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("brutalist-login.html", {"request": request})

@router.post("/login")
async def login_post(
        db: AsyncSession = Depends(get_db),
        login: str = Form(...),
        password: str = Form(...)
    ):
    try:
        user_credentials = UserLogin(
            login=login,
            password=password,
        )
    except ValueError as e:
        return RedirectResponse(f"/login?error={str(e)}", status_code=303)

    logger.info(user_credentials.dict())

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
    logger.warning(f"user.hashed_password: {user.hashed_password}")
    logger.warning(f"hashed_password (form): {user_credentials.password}")

    if not argon2.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password"
        )

    auth = get_authx()

    access_token = auth.create_access_token(uid=str(user.id))
    refresh_token = auth.create_refresh_token(uid=str(user.id))


    redirect_response = RedirectResponse("/dashboard", status_code=303)

    redirect_response.set_cookie(
        key=settings.jwt_access_cookie_name,
        value=access_token,
        httponly=True,
        samesite="none",
        secure=True,
        path="/",
    )
    redirect_response.set_cookie(
        key=settings.jwt_refresh_cookie_name,
        value=refresh_token,
        httponly=True,
        samesite="none",
        secure=True,
        path="/",
    )
    return redirect_response


# Logout API
@router.post("/logout")
async def logout(response: Response):
    logger.debug("logout POST triggered")
    response = RedirectResponse("/", status_code=303)
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
    return response
