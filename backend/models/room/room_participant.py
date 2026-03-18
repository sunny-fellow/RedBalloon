from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..base import Base


class RoomParticipant(Base):
    __tablename__ = "room_participants"

    room_id = Column(Integer, ForeignKey("rooms.room_id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    joined_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    score = Column(Integer, default=0, nullable=False)
    socket = Column(String, nullable=False)

    # -------- relações --------
    room = relationship(
        "Room",
        back_populates="participants"
    )

    user = relationship(
        "User",
        back_populates="room_participations"
    )

    messages = relationship(
        "RoomChat",
        back_populates="participant",
        cascade="all, delete"
    )

    submissions = relationship(
        "RoomSubmission",
        back_populates="participant",
        cascade="all, delete"
    )