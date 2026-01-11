from server.db.models.entries import TimeEntry
from server.core.logging_config import logger


class TimeEntriesRepository:
    def __init__(self):
        self.model = TimeEntry

    async def create(self, db, new_entry):
        entry = self.model(
            user_id=new_entry.user_id
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