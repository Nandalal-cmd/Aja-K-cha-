from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import NotificationOut
from backend.services.notification_service import (
    get_notifications,
    get_unread_count,
    mark_as_read,
    mark_all_read,
)
from backend.utils.auth import get_current_user
from backend.models import User

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("/")
async def list_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    notifs = await get_notifications(user.id, db, skip=skip, limit=limit)
    return notifs


@router.get("/unread-count")
async def unread_count(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    count = await get_unread_count(user.id, db)
    return {"count": count}


@router.post("/{notification_id}/read")
async def read_notification(
    notification_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    notif = await mark_as_read(notification_id, user.id, db)
    if not notif:
        return {"message": "Notification not found"}
    return notif


@router.post("/read-all")
async def read_all(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await mark_all_read(user.id, db)
    return {"message": "All notifications marked as read"}
