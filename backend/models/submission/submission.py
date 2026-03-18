from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..base import Base
from ..enums import SubmissionStatus, LanguageType


class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(Integer, primary_key=True, autoincrement=True)

    problem_id = Column(Integer, ForeignKey("problems.problem_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    code = Column(String, nullable=False)
    language = Column(Enum(LanguageType), nullable=False)
    time_spent = Column(Integer, nullable=False)
    memory_used = Column(Integer, nullable=False)

    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.JUDGING, nullable=False)
    submitted_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)

    # -------- relações --------

    problem = relationship(
        "Problem",
        back_populates="submissions"
    )

    user = relationship(
        "User",
        back_populates="submissions"
    )

    reacts = relationship(
        "SubmissionReact",
        back_populates="submission",
        cascade="all, delete"
    )