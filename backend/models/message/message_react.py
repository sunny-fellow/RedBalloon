from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..base import Base
from ..enums import ReactionType


class MessageReact(Base):
    __tablename__ = "message_reacts"

    message_id = Column(Integer, ForeignKey("messages.message_id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    reaction = Column(Enum(ReactionType), nullable=False)
    reacted_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)

    # -------- relações --------
    message = relationship(
        "Message",
        back_populates="likes"
    )

    user = relationship(
        "User",
        back_populates="liked_messages"
    )