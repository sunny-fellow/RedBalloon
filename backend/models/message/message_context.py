from sqlalchemy import Column, Integer, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from ..base import Base
from ..enums import MessageContextType


class MessageContext(Base):
    __tablename__ = "message_contexts"

    message_id = Column(Integer, ForeignKey("messages.message_id", ondelete="CASCADE"), primary_key=True)
    context_type = Column(Enum(MessageContextType), nullable=False)
    context_ref_id = Column(Integer, nullable=True)
    parent_message = Column(Integer, nullable=True)

    # -------- relação com Message --------
    message = relationship(
        "Message",
        back_populates="context",
        uselist=False
    )


# -------- índices --------
Index("idx_context_type_ref_id", MessageContext.context_type, MessageContext.context_ref_id)
Index("idx_parent_message", MessageContext.parent_message)