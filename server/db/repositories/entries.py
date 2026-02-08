from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from server.db.models.entries import TimeEntry
from server.core.logging_config import logger


class TimeEntriesRepository:
    def __init__(self):
        self.model = TimeEntry

    async def create(self, db: AsyncSession, new_entry):
        entry = self.model(
            user_id=new_entry.user_id,
            title=new_entry.title,
            description=new_entry.description
        )
        db.add(entry)
        try:
            await db.commit()
            await db.refresh(entry)
            logger.debug(f"Time entry {entry.id} created for user {entry.user_id}")
            return entry
        except Exception as e:
            logger.error(f"Error creating entry {entry.id} for user {entry.user_id} - {e}")
            await db.rollback()
            raise

    async def update(self, db: AsyncSession, entry_id: int, **kwargs):
        """
        Update time entry with provided fields.

        Args:
            db: Database session
            entry_id: ID of the entry to update
            **kwargs: Fields to update (title, description, started_at, ended_at)

        Returns:
            Updated TimeEntry object or None if not found

        Raises:
            Exception: If database operation fails
        """
        try:
            stmt = select(self.model).where(self.model.id == entry_id)
            result = await db.execute(stmt)
            entry = result.scalar_one_or_none()

            if not entry:
                logger.warning(f"Time entry not found for update: {entry_id}")
                return None

            updated_fields = []
            for key, value in kwargs.items():
                if hasattr(entry, key):
                    setattr(entry, key, value)
                    updated_fields.append(key)

            if updated_fields:
                await db.commit()
                await db.refresh(entry)
            else:
                logger.debug(f"No valid fields to update for {entry_id}")

            return entry
        except Exception as e:
            logger.error(f"Error updating session: {e}")
            await db.rollback()
            raise
