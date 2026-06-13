from pydantic import BaseModel
from datetime import datetime
import uuid


class ChallengeResponse(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    description: str
    difficulty: str
    points: int
    category: str
    expected_tool: str | None
    is_active: bool

    class Config:
        from_attributes = True


class ChallengeDetailResponse(ChallengeResponse):
    hint: str | None = None


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
    avatar_url: str | None
    points: int
    solved_count: int
