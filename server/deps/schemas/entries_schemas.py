from typing import Optional

from pydantic import BaseModel

class EntryCreate(BaseModel):
    user_id: int
    title: Optional[str] = None
    description: Optional[str] = None

class EntryStartRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
