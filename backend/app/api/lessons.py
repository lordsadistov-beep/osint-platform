from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from ..core.database import get_db
from ..core.dependencies import get_current_user, get_current_admin
from ..models.lesson import Lesson, UserProgress
from ..models.challenge import Challenge
from ..models.user import User
from ..schemas.lesson import (
    LessonResponse, LessonDetailResponse, CategoryResponse,
    PracticeResponse, CompleteLessonResponse, RelatedResponse
)

router = APIRouter()


@router.get("")
async def list_lessons(
    category: str = None,
    difficulty: str = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Lesson).where(Lesson.is_published == True)
    if category:
        query = query.where(Lesson.category == category)
    if difficulty:
        query = query.where(Lesson.difficulty == difficulty)
    query = query.order_by(Lesson.order_index)
    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()
    result = await db.execute(query.offset((page - 1) * limit).limit(limit))
    items = result.scalars().all()
    return {"items": [LessonResponse.from_orm(l) for l in items], "total": total, "page": page, "limit": limit}


@router.get("/categories")
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson.category, func.count().label("count"))
        .where(Lesson.is_published == True)
        .group_by(Lesson.category)
    )
    return [{"category": row[0], "count": row[1]} for row in result]


@router.get("/{slug}", response_model=LessonDetailResponse)
async def get_lesson(slug: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lesson).where(Lesson.slug == slug))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.get("/{slug}/practice", response_model=PracticeResponse)
async def get_practice(slug: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lesson).where(Lesson.slug == slug))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    example_data = f"example_{lesson.tool_slug}_data" if lesson.tool_slug else ""
    return PracticeResponse(lesson=LessonResponse.from_orm(lesson), example_data=example_data)


@router.post("/{slug}/complete", response_model=CompleteLessonResponse)
async def complete_lesson(slug: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lesson).where(Lesson.slug == slug))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    progress_result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == user.id,
            UserProgress.lesson_id == lesson.id,
        )
    )
    progress = progress_result.scalar_one_or_none()
    if not progress:
        progress = UserProgress(user_id=user.id, lesson_id=lesson.id, completed=True)
        db.add(progress)
        user.experience += lesson.xp_reward
    elif not progress.completed:
        progress.completed = True
        user.experience += lesson.xp_reward
    new_level = user.experience // 150 + 1
    if new_level > user.level:
        user.level = new_level
    db.add(user)
    await db.flush()
    return CompleteLessonResponse(xp_awarded=lesson.xp_reward, new_level=user.level)


@router.get("/{id}/related", response_model=RelatedResponse)
async def get_related(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lesson).where(Lesson.id == id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    tool = {"slug": lesson.tool_slug, "name": lesson.tool_slug} if lesson.tool_slug else None
    chal_result = await db.execute(
        select(Challenge).where(Challenge.expected_tool == lesson.tool_slug, Challenge.is_active == True).limit(5)
    )
    challenges = [{"id": str(c.id), "title": c.title, "slug": c.slug, "difficulty": c.difficulty, "points": c.points} for c in chal_result.scalars().all()]
    next_result = await db.execute(
        select(Lesson).where(Lesson.order_index > lesson.order_index, Lesson.is_published == True).order_by(Lesson.order_index).limit(1)
    )
    next_lesson = next_result.scalar_one_or_none()
    return RelatedResponse(
        tool=tool,
        challenges=challenges,
        next_lesson=LessonResponse.from_orm(next_lesson) if next_lesson else None,
    )
