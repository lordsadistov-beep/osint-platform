from pydantic import BaseModel
from datetime import datetime
import uuid


class UserResponse(BaseModel):
    id: uuid.UUID
    telegram_id: int | None
    username: str
    email: str | None
    avatar_url: str | None
    role: str
    experience: int
    level: int
    created_at: datetime

    class Config:
        orm_mode = True
