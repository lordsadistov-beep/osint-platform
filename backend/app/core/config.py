from pydantic import BaseSettings, validator
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://osint:supersecret123@localhost:5432/osint_platform"

    @validator("DATABASE_URL", pre=True)
    def ensure_async_driver(cls, v: str) -> str:
        if v and "+asyncpg" not in v.replace("postgresql+asyncpg", ""):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v
    REDIS_URL: str = "redis://localhost:6379"
    SECRET_KEY: str = "change-this-secret-key-at-least-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    TELEGRAM_BOT_TOKEN: str = ""
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    RATE_LIMIT_PER_MINUTE: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
