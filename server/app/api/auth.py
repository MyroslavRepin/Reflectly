import os

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response


from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from server.db.sessions import get_db
from server.deps.schemas.user_create import UserCreate
from server.utils.security.auth import hash_password
from server.db.repositories.users import UserRepository

router = APIRouter()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(
    BASE_DIR, "..", "..", "..", "frontend"))

templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates/routes"))

# Signup API
@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    error = request.query_params.get("error")
    return templates.TemplateResponse("brutalist-signup.html", {"request": request, "error": error})


@router.post('/signup')
async def signup_post(
    request: Request,
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
            hashed_password=hash_password(plain_password=password)
        )
        await repo.create(db, **user.dict())


        return RedirectResponse('/login', status_code=303)
    except IntegrityError:
        return RedirectResponse("/signup?error=Email+or+username+already+exists!&username=" + username + "&email=" + email, status_code=303)
    except ValueError as e:
        return RedirectResponse(f"/signup?error={str(e)}&username={username}&email={email}", status_code=303)


# Logout API
@router.post("/logout")
async def logout(response: Response):
    logger.debug("logout POST triggered")
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        path="/",
        samesite="lax",
        secure=False,
    )
    response.delete_cookie(
        key=config.JWT_REFRESH_COOKIE_NAME,
        path="/",
        samesite="lax",
        secure=False,
    )
    return response
