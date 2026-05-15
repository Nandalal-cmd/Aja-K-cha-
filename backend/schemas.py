import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from backend.models import ChallengeType


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    display_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=4, max_length=100)


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"


class UserOut(BaseModel):
    id: int
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    language: str
    bio: Optional[str] = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    language: Optional[str] = Field(None, max_length=10)


class UserProfile(UserOut):
    streak: Optional["StreakOut"] = None
    friend_count: int = 0
    post_count: int = 0


class ChallengeOut(BaseModel):
    id: int
    date: datetime.date
    title_np: str
    title_en: str
    description_np: str
    description_en: str
    challenge_type: ChallengeType
    points: int
    is_active: bool

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    caption: Optional[str] = None
    is_public: bool = True


class PostOut(BaseModel):
    id: int
    user_id: int
    challenge_id: int
    caption: Optional[str] = None
    image_path: str
    is_public: bool
    created_at: datetime.datetime
    expires_at: datetime.datetime
    user: Optional[UserOut] = None
    challenge: Optional[ChallengeOut] = None
    reactions: List["ReactionOut"] = []
    reaction_count: int = 0

    class Config:
        from_attributes = True


class FriendRequestOut(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    status: str
    created_at: datetime.datetime
    from_user: Optional[UserOut] = None
    to_user: Optional[UserOut] = None

    class Config:
        from_attributes = True


class FriendOut(BaseModel):
    id: int
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    streak: Optional["StreakOut"] = None

    class Config:
        from_attributes = True


class ReactionOut(BaseModel):
    id: int
    post_id: int
    user_id: int
    emoji: str
    created_at: datetime.datetime
    user: Optional[UserOut] = None

    class Config:
        from_attributes = True


class StreakOut(BaseModel):
    current_streak: int
    longest_streak: int
    last_post_date: Optional[datetime.date] = None

    class Config:
        from_attributes = True


class NotificationOut(BaseModel):
    id: int
    user_id: int
    message: str
    type: str
    related_id: Optional[int] = None
    is_read: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class SearchResult(BaseModel):
    users: List[UserOut] = []
