from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base


class MessageTag(Base):
    __tablename__ = "message_tags"

    message_id = Column(Integer, ForeignKey("messages.message_id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True)

    # -------- relações --------
    message = relationship(
        "Message",
        back_populates="tags"
    )

    tag = relationship(
        "Tag",
        back_populates="message_tags"
    )