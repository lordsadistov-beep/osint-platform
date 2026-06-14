from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class LessonResponse(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    description: Optional[str]
    category: str
    difficulty: str
    order_index: int
    tool_slug: Optional[str]
    xp_reward: int
    estimated_minutes: Optional[int]
    is_published: bool
    created_at: datetime

    class Config:
        orm_mode = True


class LessonDetailResponse(LessonResponse):
    content: str


class LessonProgressResponse(BaseModel):
    lesson_id: uuid.UUID
    completed: bool
    completed_at: Optional[datetime]


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
    tool: Optional[dict]
    challenges: list
    next_lesson: Optional[LessonResponse]