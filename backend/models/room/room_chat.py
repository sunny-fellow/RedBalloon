from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..base import Base


class RoomChat(Base):
    __tablename__ = "room_chats"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    sent_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['room_id', 'user_id'],
            ['room_participants.room_id', 'room_participants.user_id'],
            ondelete="CASCADE"
        ),
    )

    participant = relationship(
        "RoomParticipant",
        back_populates="messages"
    )