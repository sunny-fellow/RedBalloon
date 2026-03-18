from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base
from ..enums import MessageTags


class MessageTag(Base):
    __tablename__ = "message_tags"

    message_tag_id = Column(Integer, primary_key=True, autoincrement=True)

    message_id = Column(
        Integer,
        ForeignKey("messages.message_id", ondelete="CASCADE"),
        nullable=False
    )

    tag = Column(
        Enum(MessageTags, name="message_tags_enum"),
        nullable=False
    )

    # -------- relações --------
    message = relationship(
        "Message",
        back_populates="tags"
    )