from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..base import Base
from ..enums import RoomStatus


class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    password = Column(String, nullable=False)

    socket = Column(String, nullable=False)

    max_participants = Column(Integer, nullable=False)

    accepting_submissions = Column(Boolean, default=True)

    ends_at = Column(String, nullable=False)

    status = Column(
        Enum(RoomStatus),
        default=RoomStatus.IN_PROGRESS,
        nullable=False
    )

    # -------- relações --------

    participants = relationship(
        "RoomParticipant",
        back_populates="room",
        cascade="all, delete"
    )

    room_problems = relationship(
        "RoomProblem",
        back_populates="room",
        cascade="all, delete"
    )