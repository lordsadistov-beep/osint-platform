from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ...core.database import get_db
from ...core.dependencies import get_current_user
from ...models.user import User
from ...models.leak_entry import LeakEntry
from ...models.search_history import SearchHistory
from ...schemas.tool import LeakSearchRequest, LeakSearchResponse, LeakEntryResponse

router = APIRouter()


@router.post("/leaks/search", response_model=LeakSearchResponse)
async def search_leaks(
    req: LeakSearchRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(LeakEntry)
    if req.type == "email":
        query = query.where(LeakEntry.email == req.query)
    elif req.type == "username":
        query = query.where(LeakEntry.username == req.query)
    elif req.type == "phone":
        query = query.where(LeakEntry.phone == req.query)
    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar() or 0
    result = await db.execute(query.limit(100))
    entries = [LeakEntryResponse(
        email=e.email, username=e.username, password_hash=e.password_hash,
        password_plain=e.password_plain, source=e.source, breach_name=e.breach_name,
        ip_address=e.ip_address, phone=e.phone,
    ) for e in result.scalars().all()]
    history = SearchHistory(
        user_id=user.id, tool_slug="leaks", query=f"{req.type}:{req.query}",
        result_summary={"found": len(entries) > 0, "total": total},
    )
    db.add(history)
    await db.flush()
    return LeakSearchResponse(found=len(entries) > 0, entries=entries, total_count=total)
