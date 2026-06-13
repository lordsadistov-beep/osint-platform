from pydantic import BaseModel
from datetime import datetime
import uuid


class DashboardStats(BaseModel):
    total_searches: int
    total_connections: int
    lessons_completed: int
    challenges_solved: int
    experience: int
    level: int
    rank_percent: float


class HistoryItem(BaseModel):
    id: uuid.UUID
    tool_slug: str
    query: str
    result_summary: dict | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class PaginatedHistory(BaseModel):
    items: list[HistoryItem]
    total: int
    page: int
    limit: int


class ExportRequest(BaseModel):
    format: str = "json"
