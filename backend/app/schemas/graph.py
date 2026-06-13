from pydantic import BaseModel
import uuid
from datetime import datetime


class ConnectionResponse(BaseModel):
    id: uuid.UUID
    source_type: str
    source_value: str
    target_type: str
    target_value: str
    relationship: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
