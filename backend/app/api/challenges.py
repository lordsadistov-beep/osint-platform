from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from ..core.database import get_db
from ..core.dependencies import get_current_user
from ..core.security import get_password_hash, verify_password
from ..models.user import User
from ..models.challenge import Challenge, ChallengeSubmission
from ..schemas.challenge import (
    ChallengeResponse, ChallengeDetailResponse, SubmitFlagRequest,
    SubmitFlagResponse, HintResponse, LeaderboardEntry
)

router = APIRouter()


@router.get("")
async def list_challenges(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Challenge).where(Challenge.is_active == True))
    return {"items": [ChallengeResponse.model_validate(c) for c in result.scalars().all()]}


@router.get("/{id}", response_model=ChallengeDetailResponse)
async def get_challenge(id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Challenge).where(Challenge.id == id))
    challenge = result.scalar_one_or_none()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    sub_result = await db.execute(
        select(ChallengeSubmission).where(
            ChallengeSubmission.user_id == user.id,
            ChallengeSubmission.challenge_id == challenge.id,
            ChallengeSubmission.is_correct == True,
        )
    )
    solved = sub_result.scalar_one_or_none()
    detail = ChallengeDetailResponse.model_validate(challenge)
    if not solved:
        detail.hint = None
    return detail


@router.post("/{id}/hint", response_model=HintResponse)
async def get_hint(id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Challenge).where(Challenge.id == id))
    challenge = result.scalar_one_or_none()
    if not challenge or not challenge.hint:
        raise HTTPException(status_code=404, detail="No hint available")
    penalty = challenge.points // 2
    return HintResponse(hint=challenge.hint, penalty=penalty)


@router.post("/{id}/submit", response_model=SubmitFlagResponse)
async def submit_flag(id: str, req: SubmitFlagRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Challenge).where(Challenge.id == id))
    challenge = result.scalar_one_or_none()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    sub_result = await db.execute(
        select(ChallengeSubmission).where(
            ChallengeSubmission.user_id == user.id,
            ChallengeSubmission.challenge_id == challenge.id,
            ChallengeSubmission.is_correct == True,
        )
    )
    if sub_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already solved")
    is_correct = req.flag.strip().lower() == challenge.flag.strip().lower()
    points_awarded = challenge.points if is_correct else 0
    submission = ChallengeSubmission(
        user_id=user.id,
        challenge_id=challenge.id,
        flag_submitted=req.flag,
        is_correct=is_correct,
        points_awarded=points_awarded,
    )
    db.add(submission)
    if is_correct:
        user.experience += points_awarded
        new_level = user.experience // 150 + 1
        if new_level > user.level:
            user.level = new_level
        db.add(user)
    await db.flush()
    return SubmitFlagResponse(is_correct=is_correct, points_awarded=points_awarded)


@router.get("/leaderboard")
async def leaderboard(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            ChallengeSubmission.user_id,
            User.username,
            User.avatar_url,
            func.sum(ChallengeSubmission.points_awarded).label("points"),
            func.count(ChallengeSubmission.id).label("solved_count"),
        )
        .join(User, ChallengeSubmission.user_id == User.id)
        .where(ChallengeSubmission.is_correct == True)
        .group_by(ChallengeSubmission.user_id, User.username, User.avatar_url)
        .order_by(desc("points"))
        .limit(50)
    )
    return [LeaderboardEntry(user_id=row[0], username=row[1], avatar_url=row[2], points=row[3] or 0, solved_count=row[4] or 0) for row in result]
