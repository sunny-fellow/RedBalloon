from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship


from models.base import Base
from models.enums import ProblemTags

class ProblemTag(Base):
    __tablename__ = "problem_tags"

    problem_tag_id = Column(Integer, primary_key=True, autoincrement=True)

    problem_id = Column(
        Integer,
        ForeignKey("problems.problem_id", ondelete="CASCADE"),
        nullable=False
    )

    tag = Column(
        Enum(ProblemTags, name="problem_tags_enum"),
        nullable=False
    )

    # -------- relações --------

    problem = relationship(
        "Problem",
        back_populates="problem_tags"
    )