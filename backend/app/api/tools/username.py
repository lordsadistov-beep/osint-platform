import asyncio
import time
import aiohttp

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.dependencies import get_current_user
from ...models.user import User
from ...models.search_history import SearchHistory
from ...schemas.tool import UsernameSearchResponse, UsernameSearchResult
from typing import Optional
from typing import Optional

router = APIRouter()

SITES = {
    "github": {"url": "https://github.com/{}", "check": "status"},
    "twitter": {"url": "https://twitter.com/{}", "check": "status"},
    "instagram": {"url": "https://instagram.com/{}", "check": "status"},
    "reddit": {"url": "https://reddit.com/user/{}", "check": "status"},
    "tiktok": {"url": "https://tiktok.com/@{}", "check": "status"},
    "pinterest": {"url": "https://pinterest.com/{}", "check": "status"},
    "telegram": {"url": "https://t.me/{}", "check": "status"},
    "youtube": {"url": "https://youtube.com/@{}", "check": "status"},
    "twitch": {"url": "https://twitch.tv/{}", "check": "status"},
    "medium": {"url": "https://medium.com/@{}", "check": "status"},
    "devto": {"url": "https://dev.to/{}", "check": "status"},
    "gitlab": {"url": "https://gitlab.com/{}", "check": "status"},
    "bitbucket": {"url": "https://bitbucket.org/{}/", "check": "status"},
    "codepen": {"url": "https://codepen.io/{}", "check": "status"},
    "replit": {"url": "https://replit.com/@{}", "check": "status"},
    "stackoverflow": {"url": "https://stackoverflow.com/users?q={}", "check": "status"},
    "steam": {"url": "https://steamcommunity.com/id/{}", "check": "status"},
    "chess": {"url": "https://chess.com/member/{}", "check": "status"},
    "lichess": {"url": "https://lichess.org/@/{}", "check": "status"},
    "spotify": {"url": "https://open.spotify.com/user/{}", "check": "status"},
    "soundcloud": {"url": "https://soundcloud.com/{}", "check": "status"},
    "flickr": {"url": "https://flickr.com/people/{}", "check": "status"},
    "behance": {"url": "https://behance.net/{}", "check": "status"},
    "dribbble": {"url": "https://dribbble.com/{}", "check": "status"},
    "keybase": {"url": "https://keybase.io/{}", "check": "status"},
    "pastebin": {"url": "https://pastebin.com/u/{}", "check": "status"},
    "disqus": {"url": "https://disqus.com/by/{}", "check": "status"},
    "gravatar": {"url": "https://gravatar.com/{}", "check": "status"},
    "wordpress": {"url": "https://{}.wordpress.com", "check": "status"},
    "blogger": {"url": "https://{}.blogspot.com", "check": "status"},
}


async def check_site(session: aiohttp.ClientSession, site_name: str, site_config: dict, username: str) -> Optional[dict]:
    url = site_config["url"].format(username)
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5), allow_redirects=False) as resp:
            if resp.status == 200:
                return {"site": site_name, "url": url, "profile_exists": True}
    except Exception:
        pass
    return None


async def check_sites_ws(websocket: WebSocket, username: str):
    await websocket.accept()
    site_list = list(SITES.items())
    found = []
    checked = 0
    start_time = time.time()
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        tasks = [check_site(session, name, config, username) for name, config in site_list]
        for coro in asyncio.as_completed(tasks):
            result = await coro
            checked += 1
            if result:
                found.append(result)
            try:
                await websocket.send_json({
                    "type": "progress",
                    "checked": checked,
                    "total": len(site_list),
                    "found": len(found),
                    "current_site": site_list[checked - 1][0],
                })
            except Exception:
                break
    elapsed = int((time.time() - start_time) * 1000)
    try:
        await websocket.send_json({
            "type": "result",
            "query": username,
            "sites_checked": checked,
            "found": found,
            "not_found_count": checked - len(found),
            "elapsed_ms": elapsed,
        })
    except Exception:
        pass


@router.websocket("/username/{username}/ws")
async def username_search_ws(websocket: WebSocket, username: str):
    await check_sites_ws(websocket, username)


@router.post("/username/{username}", response_model=UsernameSearchResponse)
async def username_search(
    username: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    start_time = time.time()
    found = []
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        tasks = [check_site(session, name, config, username) for name, config in SITES.items()]
        results = await asyncio.gather(*tasks)
    for r in results:
        if r:
            found.append(UsernameSearchResult(**r))
    elapsed = int((time.time() - start_time) * 1000)
    history = SearchHistory(
        user_id=user.id,
        tool_slug="username",
        query=username,
        result_summary={"found_count": len(found), "sites_checked": len(SITES)},
    )
    db.add(history)
    await db.flush()
    return UsernameSearchResponse(
        query=username,
        sites_checked=len(SITES),
        found=found,
        not_found_count=len(SITES) - len(found),
        elapsed_ms=elapsed,
    )


