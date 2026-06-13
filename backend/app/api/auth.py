from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.database import get_db
from ..core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from ..core.dependencies import get_current_user
from ..models.user import User
from ..schemas.auth import RegisterRequest, LoginRequest, TelegramAuthRequest, TokenResponse, RefreshRequest, UpdateProfileRequest
from ..schemas.user import UserResponse

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where((User.username == req.username) | (User.email == req.email)))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    user = User(
        username=req.username,
        email=req.email,
        password_hash=get_password_hash(req.password),
    )
    db.add(user)
    await db.flush()
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where((User.username == req.username) | (User.email == req.username))
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/telegram", response_model=TokenResponse)
async def telegram_auth(req: TelegramAuthRequest, db: AsyncSession = Depends(get_db)):
    import hmac
    import hashlib
    secret = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
    check_str = f"auth_date={req.auth_date}\nfirst_name={req.first_name}\nid={req.telegram_id}"
    if req.last_name:
        check_str += f"\nlast_name={req.last_name}"
    if req.photo_url:
        check_str += f"\nphoto_url={req.photo_url}"
    computed_hash = hmac.new(secret, check_str.encode(), hashlib.sha256).hexdigest()
    if computed_hash != req.hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Telegram auth")
    result = await db.execute(select(User).where(User.telegram_id == req.telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        import random
        base_username = f"tg_{req.telegram_id}"
        username = base_username
        while (await db.execute(select(User).where(User.username == username))).scalar_one_or_none():
            username = f"{base_username}_{random.randint(100, 999)}"
        user = User(
            telegram_id=req.telegram_id,
            username=username,
            avatar_url=req.photo_url or None,
        )
        db.add(user)
        await db.flush()
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(req: RefreshRequest):
    payload = decode_token(req.refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    access_token = create_access_token({"sub": payload["sub"]})
    new_refresh_token = create_refresh_token({"sub": payload["sub"]})
    return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserResponse)
async def update_me(req: UpdateProfileRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if req.username:
        user.username = req.username
    if req.email:
        user.email = req.email
    if req.avatar_url is not None:
        user.avatar_url = req.avatar_url
    db.add(user)
    await db.flush()
    return user
