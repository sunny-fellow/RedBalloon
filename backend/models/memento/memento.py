from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..base import Base


class Memento(Base):
    __tablename__ = "mementos"

    memento_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True, default=None)

    entity_class = Column(String, nullable=False)
    entity_pk = Column(String, nullable=False)

    action = Column(String, nullable=False)

    snapshot = Column(JSON, nullable=True)

    created_at = Column(
        String,
        nullable=False,
        default=lambda: datetime.now(timezone.utc).isoformat()
    )

    user = relationship("User", back_populates="mementos")