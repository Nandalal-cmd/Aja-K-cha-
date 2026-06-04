from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from backend.database import get_db
from backend.schemas import UserRegister, UserLogin, UserUpdate, PasswordChange, UserOut, TokenResponse, UserProfile
from backend.services.auth_service import register_user, login_user, update_user, change_password
from backend.utils.auth import get_current_user
from backend.utils.helpers import save_avatar, delete_file
from backend.utils.config import UPLOAD_DIR
from backend.models import User
from backend.services.friend_service import get_friends
from backend.services.post_service import get_user_posts

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    return await register_user(data, db)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login_user(data, db)


@router.get("/me", response_model=UserProfile)
async def get_me(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    friends = await get_friends(user.id, db)
    posts = await get_user_posts(user.id, db)
    return UserProfile(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        language=user.language,
        bio=user.bio,
        created_at=user.created_at,
        streak=user.streak,
        friend_count=len(friends),
        post_count=len(posts),
    )


@router.put("/me", response_model=UserProfile)
async def update_me(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user = await update_user(user, data, db)
    friends = await get_friends(user.id, db)
    posts = await get_user_posts(user.id, db)
    return UserProfile(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        language=user.language,
        bio=user.bio,
        created_at=user.created_at,
        streak=user.streak,
        friend_count=len(friends),
        post_count=len(posts),
    )


@router.post("/change-password")
async def change_user_password(
    data: PasswordChange,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await change_password(user, data, db)


@router.post("/avatar", response_model=UserProfile)
async def upload_avatar(
    image: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    if user.avatar_url:
        old_path = str(UPLOAD_DIR / Path(user.avatar_url).name)
        delete_file(old_path)

    file_path = await save_avatar(image)
    relative_path = Path(file_path).name
    user.avatar_url = relative_path
    await db.commit()
    await db.refresh(user)

    friends = await get_friends(user.id, db)
    posts = await get_user_posts(user.id, db)
    return UserProfile(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        language=user.language,
        bio=user.bio,
        created_at=user.created_at,
        streak=user.streak,
        friend_count=len(friends),
        post_count=len(posts),
    )
