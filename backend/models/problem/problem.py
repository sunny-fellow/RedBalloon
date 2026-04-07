from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..base import Base
from ..enums import ProblemDifficulty, ValidationMode

class Problem(Base):
    __tablename__ = "problems"

    problem_id = Column(Integer, primary_key=True, autoincrement=True)

    creator_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    time_limit = Column(Integer, nullable=False)
    memory_limit = Column(Integer, nullable=False)

    validation_mode = Column(Enum(ValidationMode), nullable=False)
    difficulty = Column(Enum(ProblemDifficulty), nullable=False)

    private = Column(Boolean, default=False, nullable=False)
    created_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat(), nullable=False)

    # Relações
    creator = relationship(
        "User",
        back_populates="problems_created"
    )

    room_problems = relationship(
        "RoomProblem",
        back_populates="problem",
        cascade="all, delete"
    )

    room_submissions = relationship(
        "RoomSubmission",
        back_populates="problem",
        cascade="all, delete"
    )

    submissions = relationship(
        "Submission",
        back_populates="problem",
        cascade="all, delete"
    )

    test_cases = relationship(
        "ProblemTestCase",
        back_populates="problem",
        cascade="all, delete"
    )

    inputs = relationship(
        "ProblemInput",
        back_populates="problem",
        cascade="all, delete"
    )

    checker = relationship(
        "ProblemChecker",
        back_populates="problem"
    )

    problem_tags = relationship(
        "ProblemTag",
        back_populates="problem"
    )

    reactions = relationship(
        "ProblemReact",
        back_populates="problem",
        cascade="all, delete"
    )