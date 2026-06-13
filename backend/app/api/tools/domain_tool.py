from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.dependencies import get_current_user
from ...models.user import User
from ...models.search_history import SearchHistory
from ...schemas.tool import DomainLookupResponse

router = APIRouter()


@router.post("/domain/{domain}", response_model=DomainLookupResponse)
async def domain_lookup(
    domain: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    import socket
    ip = None
    try:
        ip = socket.gethostbyname(domain)
    except Exception:
        pass
    result = DomainLookupResponse(
        domain=domain,
        dns={"a": [ip] if ip else []},
        ip=ip,
        subdomains=[],
    )
    history = SearchHistory(
        user_id=user.id, tool_slug="domain", query=domain, result_summary={"ip": ip}
    )
    db.add(history)
    await db.flush()
    return result
