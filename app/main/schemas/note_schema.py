from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateNote(BaseModel):
    title: str
    description: str
    status: Optional[str] = "PENDING"
    target_date: datetime
    user_id: int


class UpdateNote(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str] = "PENDING"
    target_date: Optional[datetime]
