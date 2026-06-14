from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import Optional


class UserResponse(BaseModel):
    id: uuid.UUID
    telegram_id: Optional[int]
    username: str
    email: Optional[str]
    avatar_url: Optional[str]
    role: str
    experience: int
    level: int
    created_at: datetime

    class Config:
        orm_mode = True


