from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from ..base import Base
from models.enums import LanguageType

class ProblemChecker(Base):
    __tablename__ = "problem_checkers"

    checker_id = Column(Integer, primary_key=True, autoincrement=True)

    problem_id = Column(
        Integer,
        ForeignKey("problems.problem_id", ondelete="CASCADE"),
        nullable=False
    )

    language = Column(Enum(LanguageType), nullable=False)
    source_code = Column(String, nullable=False)

    problem = relationship(
        "Problem",
        back_populates="checker"
    )