from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Base


class ProblemTestCase(Base):
    __tablename__ = "problem_test_cases"

    test_case_id = Column(Integer, primary_key=True, autoincrement=True)

    problem_id = Column(
        Integer,
        ForeignKey("problems.problem_id", ondelete="CASCADE"),
        nullable=False
    )

    input_data = Column(String, nullable=False)
    output_data = Column(String, nullable=False)

    problem = relationship(
        "Problem",
        back_populates="test_cases"
    )