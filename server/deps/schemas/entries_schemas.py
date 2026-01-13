from pydantic import BaseModel

# Currently I don't need schemas :)
class EntryCreate(BaseModel):
    user_id: int
