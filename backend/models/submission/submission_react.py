from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..base import Base
from ..enums import ReactionType


class SubmissionReact(Base):
    __tablename__ = "submission_reacts"

    submission_id = Column(Integer, ForeignKey("submissions.submission_id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    reaction = Column(Enum(ReactionType), nullable=False)
    reacted_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)

    # -------- relações --------
    submission = relationship(
        "Submission",
        back_populates="reacts"
    )

    user = relationship(
        "User",
        back_populates="liked_submissions"
    )