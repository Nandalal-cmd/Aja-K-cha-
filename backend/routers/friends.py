from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import UserOut, FriendRequestOut, FriendOut
from backend.services.friend_service import (
    search_users,
    send_request,
    accept_request,
    reject_request,
    get_friends,
    get_pending_requests,
)
from backend.utils.auth import get_current_user
from backend.models import User

router = APIRouter(prefix="/api/friends", tags=["Friends"])


@router.get("/search")
async def search(
    q: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    users = await search_users(q, user.id, db, skip=skip, limit=limit)
    return {"users": users}


@router.post("/request/{to_user_id}")
async def send_friend_request(
    to_user_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if to_user_id == user.id:
        raise HTTPException(status_code=400, detail="Cannot add yourself")

    req = await send_request(user.id, to_user_id, db)
    if not req:
        raise HTTPException(status_code=400, detail="Request already sent or already friends")
    return req


@router.post("/accept/{request_id}")
async def accept_friend_request(
    request_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    req = await accept_request(request_id, user.id, db)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return {"message": "Friend request accepted"}


@router.post("/reject/{request_id}")
async def reject_friend_request(
    request_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    req = await reject_request(request_id, user.id, db)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return {"message": "Friend request rejected"}


@router.get("/list")
async def friends_list(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    friends = await get_friends(user.id, db)
    return friends


@router.get("/requests")
async def pending_requests(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    requests = await get_pending_requests(user.id, db)
    return requests
