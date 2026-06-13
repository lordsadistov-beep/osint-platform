import asyncio
import aiohttp

SITES = {
    "github": "https://github.com/{}",
    "twitter": "https://twitter.com/{}",
    "instagram": "https://instagram.com/{}",
    "reddit": "https://reddit.com/user/{}",
    "tiktok": "https://tiktok.com/@{}",
    "telegram": "https://t.me/{}",
    "youtube": "https://youtube.com/@{}",
}


async def check_site(session: aiohttp.ClientSession, name: str, url_template: str, username: str) -> dict | None:
    url = url_template.format(username)
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            if resp.status == 200:
                return {"site": name, "url": url, "profile_exists": True}
    except Exception:
        pass
    return None


async def search_username(username: str) -> list[dict]:
    found = []
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        tasks = [check_site(session, name, url, username) for name, url in SITES.items()]
        results = await asyncio.gather(*tasks)
    for r in results:
        if r:
            found.append(r)
    return found
