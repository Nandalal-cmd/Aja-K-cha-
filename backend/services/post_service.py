import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from sqlalchemy.orm import selectinload

from backend.models import Post, User, DailyChallenge, Reaction, Streak
from backend.schemas import PostCreate
from backend.utils.helpers import save_upload, get_expiry_time, delete_file


async def create_post(
    user_id: int,
    challenge_id: int,
    data: PostCreate,
    file,
    db: AsyncSession,
) -> Post:
    image_path = await save_upload(file)

    post = Post(
        user_id=user_id,
        challenge_id=challenge_id,
        caption=data.caption,
        image_path=image_path,
        is_public=data.is_public,
        expires_at=get_expiry_time(24),
    )
    db.add(post)

    await _update_streak(user_id, db)
    await db.commit()
    await db.refresh(post)
    result = await db.execute(
        select(Post)
        .options(
            selectinload(Post.user),
            selectinload(Post.challenge),
            selectinload(Post.reactions),
        )
        .where(Post.id == post.id)
    )
    return result.scalar_one()


async def _update_streak(user_id: int, db: AsyncSession):
    today = datetime.date.today()
    result = await db.execute(select(Streak).where(Streak.user_id == user_id))
    streak = result.scalar_one_or_none()

    if not streak:
        streak = Streak(user_id=user_id)
        db.add(streak)

    if streak.last_post_date == today:
        return

    if streak.last_post_date == today - datetime.timedelta(days=1):
        streak.current_streak += 1
    else:
        streak.current_streak = 1

    streak.longest_streak = max(streak.longest_streak, streak.current_streak)
    streak.last_post_date = today


async def get_feed(user_id: int, db: AsyncSession, skip: int = 0, limit: int = 20) -> list:
    now = datetime.datetime.utcnow()

    subq = select(User.id).where(
        User.id == user_id
    ).cte("user_friends")

    friend_ids = await db.execute(
        select(User.id).join(
            subq,
            and_(
                User.id != user_id,
            ),
            isouter=True,
        )
    )

    from backend.models import FriendRequest, FriendStatus

    sent = select(FriendRequest.to_user_id).where(
        FriendRequest.from_user_id == user_id,
        FriendRequest.status == FriendStatus.ACCEPTED,
    )
    received = select(FriendRequest.from_user_id).where(
        FriendRequest.to_user_id == user_id,
        FriendRequest.status == FriendStatus.ACCEPTED,
    )

    visible_users = {user_id}
    friend_result = await db.execute(sent)
    for row in friend_result:
        visible_users.add(row[0])
    friend_result = await db.execute(received)
    for row in friend_result:
        visible_users.add(row[0])

    result = await db.execute(
        select(Post)
        .options(
            selectinload(Post.user),
            selectinload(Post.challenge),
            selectinload(Post.reactions).selectinload(Reaction.user),
        )
        .where(
            Post.user_id.in_(visible_users),
            Post.expires_at > now,
        )
        .order_by(desc(Post.created_at))
        .offset(skip)
        .limit(limit)
    )

    posts = result.scalars().all()
    out = []
    for p in posts:
        r_count = len(p.reactions)
        out.append({
            "id": p.id,
            "user_id": p.user_id,
            "challenge_id": p.challenge_id,
            "caption": p.caption,
            "image_path": p.image_path,
            "is_public": p.is_public,
            "created_at": p.created_at,
            "expires_at": p.expires_at,
            "user": p.user,
            "challenge": p.challenge,
            "reactions": p.reactions,
            "reaction_count": r_count,
        })
    return out


async def add_reaction(post_id: int, user_id: int, emoji: str, db: AsyncSession):
    existing = await db.execute(
        select(Reaction).where(
            Reaction.post_id == post_id,
            Reaction.user_id == user_id,
        )
    )
    if existing.scalar_one_or_none():
        return

    reaction = Reaction(post_id=post_id, user_id=user_id, emoji=emoji)
    db.add(reaction)
    await db.commit()
    await db.refresh(reaction)
    return reaction


async def get_user_posts(user_id: int, db: AsyncSession, skip: int = 0, limit: int = 20) -> list:
    now = datetime.datetime.utcnow()
    result = await db.execute(
        select(Post)
        .options(
            selectinload(Post.challenge),
            selectinload(Post.reactions).selectinload(Reaction.user),
        )
        .where(Post.user_id == user_id, Post.expires_at > now)
        .order_by(desc(Post.created_at))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_post_by_id(post_id: int, db: AsyncSession):
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()


async def delete_post(post_id: int, user_id: int, db: AsyncSession) -> bool:
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.user_id == user_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        return False

    delete_file(post.image_path)
    await db.delete(post)
    await db.commit()
    return True


async def delete_expired_posts(db: AsyncSession):
    now = datetime.datetime.utcnow()
    result = await db.execute(
        select(Post).where(Post.expires_at <= now)
    )
    posts = result.scalars().all()
    for post in posts:
        delete_file(post.image_path)
        await db.delete(post)
    await db.commit()
    return len(posts)
