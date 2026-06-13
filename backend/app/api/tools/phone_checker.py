from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.dependencies import get_current_user
from ...models.user import User
from ...models.search_history import SearchHistory
from ...schemas.tool import PhoneCheckResponse

router = APIRouter()


@router.post("/phone/{phone}", response_model=PhoneCheckResponse)
async def phone_check(
    phone: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = PhoneCheckResponse(
        phone=phone,
        country="RU",
        carrier="Unknown",
        messengers={"telegram": False, "whatsapp": False, "viber": False},
        breaches=[],
    )
    history = SearchHistory(
        user_id=user.id, tool_slug="phone", query=phone, result_summary={"country": "RU"}
    )
    db.add(history)
    await db.flush()
    return result
