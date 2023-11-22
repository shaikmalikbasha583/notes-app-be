from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateNote(BaseModel):
    title: str
    description: str
    status: Optional[str] = "PENDING"
    target_date: datetime
