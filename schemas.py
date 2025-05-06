from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EntryBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []

class EntryCreate(EntryBase):
    pass

class EntryOut(EntryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
