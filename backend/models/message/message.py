from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..base import Base


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    message = Column(String, nullable=False)
    sent_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)

    # -------- relações --------
    user = relationship(
        "User",
        back_populates="messages"
    )

    context = relationship(
        "MessageContext",
        back_populates="message",
        uselist=False
    )

    likes = relationship(
        "MessageReact",
        back_populates="message",
        cascade="all, delete"
    )

    tags = relationship(
        "MessageTag",
        back_populates="message",
        cascade="all, delete"
    )