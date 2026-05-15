import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Date, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from backend.database import Base


class ChallengeType(str, enum.Enum):
    FUNNY = "funny"
    SOCIAL = "social"
    CRAZY = "crazy"
    WHOLESOME = "wholesome"
    TALENT = "talent"
    FOOD = "food"


class FriendStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    language = Column(String(10), default="ne")
    bio = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    streak = relationship("Streak", uselist=False, back_populates="user", cascade="all, delete-orphan")
    sent_requests = relationship("FriendRequest", foreign_keys="FriendRequest.from_user_id", back_populates="from_user", cascade="all, delete-orphan")
    received_requests = relationship("FriendRequest", foreign_keys="FriendRequest.to_user_id", back_populates="to_user", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="user", cascade="all, delete-orphan")


class DailyChallenge(Base):
    __tablename__ = "daily_challenges"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True, nullable=False, default=datetime.date.today)
    title_np = Column(String(200), nullable=False)
    title_en = Column(String(200), nullable=False)
    description_np = Column(Text, nullable=False)
    description_en = Column(Text, nullable=False)
    challenge_type = Column(SAEnum(ChallengeType), default=ChallengeType.FUNNY)
    points = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    posts = relationship("Post", back_populates="challenge")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("daily_challenges.id"), nullable=False)
    caption = Column(Text, nullable=True)
    image_path = Column(String(500), nullable=False)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="posts")
    challenge = relationship("DailyChallenge", back_populates="posts")
    reactions = relationship("Reaction", back_populates="post", cascade="all, delete-orphan")


class FriendRequest(Base):
    __tablename__ = "friend_requests"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SAEnum(FriendStatus), default=FriendStatus.PENDING)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_requests")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_requests")


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    emoji = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    post = relationship("Post", back_populates="reactions")
    user = relationship("User", back_populates="reactions")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(300), nullable=False)
    type = Column(String(30), nullable=False)
    related_id = Column(Integer, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id])


class Streak(Base):
    __tablename__ = "streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_post_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="streak")
