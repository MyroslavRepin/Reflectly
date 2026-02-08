from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class EntryCreate(BaseModel):
    user_id: int
    title: Optional[str] = None
    description: Optional[str] = None

class EntryStartRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class EntryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    started_at: Optional[str] = None  # ISO format
    ended_at: Union[str, None] = Field(default=...)  # ISO format or null to clear
    project_id: Optional[int] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class EntryResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str] = None
    description: Optional[str] = None

    model_config = {
        "from_attributes": True,
    }