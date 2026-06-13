from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.user import User
from ..core.security import get_password_hash, verify_password, create_access_token, create_refresh_token


async def register_user(db: AsyncSession, username: str, email: str, password: str) -> dict:
    existing = await db.execute(select(User).where((User.username == username) | (User.email == email)))
    if existing.scalar_one_or_none():
        raise ValueError("Username or email already exists")
    user = User(username=username, email=email, password_hash=get_password_hash(password))
    db.add(user)
    await db.flush()
    return {
        "access_token": create_access_token({"sub": str(user.id)}),
        "refresh_token": create_refresh_token({"sub": str(user.id)}),
    }
