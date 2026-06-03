from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload

from backend.models import FriendRequest, FriendStatus, User, Streak
from backend.services.notification_service import create_notification


async def search_users(query: str, current_user_id: int, db: AsyncSession, skip: int = 0, limit: int = 20) -> list:
    result = await db.execute(
        select(User).where(
            User.id != current_user_id,
            or_(
                User.username.ilike(f"%{query}%"),
                User.display_name.ilike(f"%{query}%"),
            ),
        ).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def send_request(from_user_id: int, to_user_id: int, db: AsyncSession):
    existing = await db.execute(
        select(FriendRequest).where(
            or_(
                and_(
                    FriendRequest.from_user_id == from_user_id,
                    FriendRequest.to_user_id == to_user_id,
                ),
                and_(
                    FriendRequest.from_user_id == to_user_id,
                    FriendRequest.to_user_id == from_user_id,
                ),
            ),
            FriendRequest.status.in_([FriendStatus.PENDING, FriendStatus.ACCEPTED]),
        )
    )
    if existing.scalar_one_or_none():
        return None

    req = FriendRequest(from_user_id=from_user_id, to_user_id=to_user_id)
    db.add(req)
    await db.flush()

    from_user_result = await db.execute(select(User).where(User.id == from_user_id))
    from_user = from_user_result.scalar_one()
    message = f"{from_user.display_name} sent you a friend request"
    await create_notification(to_user_id, message, "friend_request", db, related_id=req.id)

    await db.commit()
    await db.refresh(req)
    await db.refresh(req, ["from_user", "to_user"])
    return req


async def accept_request(request_id: int, user_id: int, db: AsyncSession):
    result = await db.execute(
        select(FriendRequest).where(
            FriendRequest.id == request_id,
            FriendRequest.to_user_id == user_id,
        )
    )
    req = result.scalar_one_or_none()
    if not req:
        return None

    req.status = FriendStatus.ACCEPTED
    await db.flush()

    to_user_result = await db.execute(select(User).where(User.id == user_id))
    to_user = to_user_result.scalar_one()
    message = f"{to_user.display_name} accepted your friend request"
    await create_notification(req.from_user_id, message, "friend_accepted", db, related_id=req.id)

    await db.commit()
    return req


async def reject_request(request_id: int, user_id: int, db: AsyncSession):
    result = await db.execute(
        select(FriendRequest).where(
            FriendRequest.id == request_id,
            FriendRequest.to_user_id == user_id,
        )
    )
    req = result.scalar_one_or_none()
    if not req:
        return None

    req.status = FriendStatus.REJECTED
    await db.commit()
    return req


async def get_friends(user_id: int, db: AsyncSession) -> list:
    sent = select(FriendRequest.to_user_id).where(
        FriendRequest.from_user_id == user_id,
        FriendRequest.status == FriendStatus.ACCEPTED,
    )
    received = select(FriendRequest.from_user_id).where(
        FriendRequest.to_user_id == user_id,
        FriendRequest.status == FriendStatus.ACCEPTED,
    )

    friend_ids = set()
    result = await db.execute(sent)
    for row in result:
        friend_ids.add(row[0])
    result = await db.execute(received)
    for row in result:
        friend_ids.add(row[0])

    if not friend_ids:
        return []

    friends = await db.execute(
        select(User).options(selectinload(User.streak)).where(User.id.in_(friend_ids))
    )
    return friends.scalars().all()


async def remove_friend(user_id: int, friend_id: int, db: AsyncSession) -> bool:
    result = await db.execute(
        select(FriendRequest).where(
            or_(
                and_(
                    FriendRequest.from_user_id == user_id,
                    FriendRequest.to_user_id == friend_id,
                ),
                and_(
                    FriendRequest.from_user_id == friend_id,
                    FriendRequest.to_user_id == user_id,
                ),
            ),
            FriendRequest.status == FriendStatus.ACCEPTED,
        )
    )
    req = result.scalar_one_or_none()
    if not req:
        return False

    await db.delete(req)
    await db.commit()
    return True


async def get_pending_requests(user_id: int, db: AsyncSession) -> list:
    result = await db.execute(
        select(FriendRequest)
        .options(
            selectinload(FriendRequest.from_user),
        )
        .where(
            FriendRequest.to_user_id == user_id,
            FriendRequest.status == FriendStatus.PENDING,
        )
        .order_by(FriendRequest.created_at.desc())
    )
    return result.scalars().all()
