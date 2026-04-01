from sqlalchemy import Column, Integer, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship

from ..base import Base
from ..enums import ReactionType

class ProblemReact(Base):
    __tablename__ = "problem_reacts"

    problem_react_id = Column(Integer, primary_key=True, autoincrement=True)

    problem_id = Column(
        Integer,
        ForeignKey("problems.problem_id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    reaction = Column(
        Enum(ReactionType),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("problem_id", "user_id", name="unique_problem_user_reaction"),
    )

    # Relações
    problem = relationship(
        "Problem",
        back_populates="reactions"
    )

    user = relationship(
        "User",
        back_populates="problem_reactions"
    )