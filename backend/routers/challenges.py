from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import ChallengeOut
from backend.services.challenge_service import get_today_challenge, get_challenge_by_id
from backend.utils.auth import get_current_user
from backend.models import User

router = APIRouter(prefix="/api/challenges", tags=["Challenges"])


@router.get("/today", response_model=ChallengeOut)
async def today_challenge(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    challenge = await get_today_challenge(db)
    if not challenge:
        raise HTTPException(status_code=404, detail="No challenge for today")
    return challenge


@router.get("/{challenge_id}", response_model=ChallengeOut)
async def get_challenge(
    challenge_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    challenge = await get_challenge_by_id(challenge_id, db)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge
