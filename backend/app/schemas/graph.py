from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional


class ConnectionResponse(BaseModel):
    id: uuid.UUID
    source_type: str
    source_value: str
    target_type: str
    target_value: str
    relationship: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


