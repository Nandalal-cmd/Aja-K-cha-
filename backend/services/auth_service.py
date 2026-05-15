from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from fastapi import HTTPException, status

from backend.models import User, Streak
from backend.schemas import UserRegister, UserLogin, UserUpdate
from backend.utils.auth import hash_password, verify_password, create_token


async def register_user(data: UserRegister, db: AsyncSession):
    existing = await db.execute(
        select(User).where(User.username == data.username)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        username=data.username,
        display_name=data.display_name,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    await db.flush()

    streak = Streak(user_id=user.id)
    db.add(streak)
    await db.commit()
    await db.refresh(user)

    token = create_token(user.id, user.username)
    return {"access_token": token, "token_type": "bearer", "user": user}


async def login_user(data: UserLogin, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.username == data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_token(user.id, user.username)
    return {"access_token": token, "token_type": "bearer", "user": user}


async def update_user(user: User, data: UserUpdate, db: AsyncSession):
    if data.display_name is not None:
        user.display_name = data.display_name
    if data.bio is not None:
        user.bio = data.bio
    if data.phone is not None:
        user.phone = data.phone
    if data.language is not None:
        user.language = data.language
    await db.commit()
    await db.refresh(user)
    return user
