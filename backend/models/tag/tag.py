from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from ..base import Base
from ..enums import TagType


class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)

    type = Column(
        Enum(TagType),
        nullable=False
    )

    message_tags = relationship(
        "MessageTag",
        back_populates="tag",
        cascade="all, delete"
    )