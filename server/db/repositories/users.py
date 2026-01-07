from sqlalchemy.ext.asyncio.session import AsyncSession

from server.db.models.users import User
from server.core.logging_config import logger

class UserRepository:
    def __init__(self):
        self.model = User

    async def create(self, db: AsyncSession, **kwargs):
        user = self.model(**kwargs)
        db.add(user)
        try:
            await db.commit()
            await db.refresh(user)
            logger.debug(f"User {user.username} created")
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            await db.rollback()
            raise
