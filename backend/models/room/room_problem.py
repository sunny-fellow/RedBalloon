from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base


class RoomProblem(Base):
    __tablename__ = "room_problems"

    room_id = Column(Integer, ForeignKey("rooms.room_id", ondelete="CASCADE"), primary_key=True)
    problem_id = Column(Integer, ForeignKey("problems.problem_id", ondelete="CASCADE"), primary_key=True)

    # -------- relações --------
    room = relationship(
        "Room",
        back_populates="room_problems"
    )

    problem = relationship(
        "Problem",
        back_populates="room_problems"
    )