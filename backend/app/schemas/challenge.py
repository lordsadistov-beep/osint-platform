from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import Optional


class ChallengeResponse(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    description: str
    difficulty: str
    points: int
    category: str
    expected_tool: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True


class ChallengeDetailResponse(ChallengeResponse):
    hint: Optional[str] = None


class SubmitFlagRequest(BaseModel):
    flag: str


class SubmitFlagResponse(BaseModel):
    is_correct: bool
    points_awarded: int


class HintResponse(BaseModel):
    hint: str
    penalty: int


class LeaderboardEntry(BaseModel):
    user_id: uuid.UUID
    username: str
    avatar_url: Optional[str]
    points: int
    solved_count: int


