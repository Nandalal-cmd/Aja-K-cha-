from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backend.database import get_db
from backend.schemas import PostCreate, PostOut, ReactionOut
from backend.services.post_service import create_post, get_feed, add_reaction, get_user_posts
from backend.services.challenge_service import get_today_challenge, get_challenge_by_id
from backend.services.notification_service import create_notification
from backend.utils.auth import get_current_user
from backend.models import User

router = APIRouter(prefix="/api/posts", tags=["Posts"])


@router.post("/upload", response_model=PostOut)
async def upload_post(
    challenge_id: int = Form(...),
    caption: Optional[str] = Form(None),
    is_public: bool = Form(True),
    image: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    challenge = await get_challenge_by_id(challenge_id, db)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    data = PostCreate(caption=caption, is_public=is_public)
    post = await create_post(user.id, challenge_id, data, image, db)
    return post


@router.get("/feed")
async def feed(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    posts = await get_feed(user.id, db, skip=skip, limit=limit)
    return posts


@router.get("/my")
async def my_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    posts = await get_user_posts(user.id, db, skip=skip, limit=limit)
    return posts


@router.post("/{post_id}/react", response_model=ReactionOut)
async def react_to_post(
    post_id: int,
    emoji: str = Form("🔥"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    reaction = await add_reaction(post_id, user.id, emoji, db)
    if not reaction:
        raise HTTPException(status_code=400, detail="Already reacted")

    from backend.services.post_service import get_post_by_id
    post = await get_post_by_id(post_id, db)
    if post and post.user_id != user.id:
        message = f"{user.display_name} reacted {emoji} to your post"
        await create_notification(
            post.user_id, message, "reaction", db, related_id=post_id
        )

    return reaction
