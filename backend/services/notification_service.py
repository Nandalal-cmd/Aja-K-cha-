import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from backend.models import Notification


async def create_notification(
    user_id: int,
    message: str,
    type: str,
    db: AsyncSession,
    related_id: int = None,
):
    notif = Notification(
        user_id=user_id,
        message=message,
        type=type,
        related_id=related_id,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(notif)
    await db.commit()
    return notif


async def get_notifications(
    user_id: int,
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50,
):
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(desc(Notification.created_at))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_unread_count(user_id: int, db: AsyncSession) -> int:
    result = await db.execute(
        select(Notification).where(
            Notification.user_id == user_id,
            Notification.is_read == False,
        )
    )
    return len(result.scalars().all())


async def mark_as_read(notification_id: int, user_id: int, db: AsyncSession):
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == user_id,
        )
    )
    notif = result.scalar_one_or_none()
    if not notif:
        return None
    notif.is_read = True
    await db.commit()
    return notif


async def mark_all_read(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(Notification).where(
            Notification.user_id == user_id,
            Notification.is_read == False,
        )
    )
    for n in result.scalars().all():
        n.is_read = True
    await db.commit()
