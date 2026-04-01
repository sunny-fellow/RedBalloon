from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..base import Base
from ..enums import SubmissionStatus, LanguageType

class RoomSubmission(Base):
    __tablename__ = "room_submissions"

    room_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.problem_id", ondelete="CASCADE"), primary_key=True)

    submitted_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)
    time_taken = Column(Integer, nullable=False)
    code = Column(String, nullable=False)
    language = Column(Enum(LanguageType), nullable=False)
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.JUDGING, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['room_id', 'user_id'],
            ['room_participants.room_id', 'room_participants.user_id'],
            ondelete="CASCADE"
        ),
    )

    # Relações
    problem = relationship(
        "Problem",
        back_populates="room_submissions"
    )

    participant = relationship(
        "RoomParticipant",
        back_populates="submissions"
    )