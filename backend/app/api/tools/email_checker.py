from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.dependencies import get_current_user
from ...models.user import User
from ...models.search_history import SearchHistory
from ...schemas.tool import EmailCheckResponse

router = APIRouter()


@router.post("/email/{email}", response_model=EmailCheckResponse)
async def email_check(
    email: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    import hashlib
    email_lower = email.lower().strip()
    gravatar_hash = hashlib.md5(email_lower.encode()).hexdigest()
    gravatar_url = f"https://gravatar.com/avatar/{gravatar_hash}?d=404"
    domain = email_lower.split("@")[1] if "@" in email_lower else ""
    result = EmailCheckResponse(
        email=email_lower,
        gravatar=gravatar_url,
        breaches=[],
        associated_sites=[],
        domain_info={"domain": domain} if domain else None,
    )
    history = SearchHistory(
        user_id=user.id, tool_slug="email", query=email_lower, result_summary={"domain": domain}
    )
    db.add(history)
    await db.flush()
    return result
