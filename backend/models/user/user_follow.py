from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..base import Base


class UserFollow(Base):
    __tablename__ = "user_follows"

    follower_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    following_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    followed_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)

    # -------- relações --------
    follower = relationship(
        "User",
        back_populates="followings",
        foreign_keys=[follower_id]
    )

    following = relationship(
        "User",
        back_populates="followers",
        foreign_keys=[following_id]
    )