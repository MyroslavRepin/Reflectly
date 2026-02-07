from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.db.repositories.users import UserRepository
from server.db.sessions import get_db
from server.deps.auth_deps import get_current_user
from server.core.logging_config import logger
from server.deps.schemas.users_schemes import UpdateUser

router = APIRouter()

user_repo = UserRepository()

@router.patch("/api/v1/users/me")
async def update_user(user_data: UpdateUser, db: AsyncSession = Depends(get_db), jwt_decoded: str = Depends(get_current_user)):
    user_id = int(jwt_decoded["user_id"])
    logger.debug(f"Updating user {jwt_decoded['user_id']}")
    user = await user_repo.update(db, user_id, **user_data.dict())
    return user