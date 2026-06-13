from pydantic import BaseModel
from datetime import datetime
import uuid


class LessonResponse(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    description: str | None
    category: str
    difficulty: str
    order_index: int
    tool_slug: str | None
    xp_reward: int
    estimated_minutes: int | None
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LessonDetailResponse(LessonResponse):
    content: str


class LessonProgressResponse(BaseModel):
    lesson_id: uuid.UUID
    completed: bool
    completed_at: datetime | None


class CategoryResponse(BaseModel):
    category: str
    count: int


class PracticeResponse(BaseModel):
    lesson: LessonResponse
    example_data: str


class CompleteLessonResponse(BaseModel):
    xp_awarded: int
    new_level: int


class RelatedResponse(BaseModel):
    tool: dict | None
    challenges: list
    next_lesson: LessonResponse | None
