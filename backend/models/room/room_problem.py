from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from ..base import Base

class RoomProblem(Base):
    __tablename__ = "room_problems"

    room_id = Column(Integer, ForeignKey("rooms.room_id", ondelete="CASCADE"), primary_key=True)
    problem_id = Column(Integer, ForeignKey("problems.problem_id", ondelete="CASCADE"), primary_key=True)

    points = Column(Integer, nullable=False, default=0)
    balloon = Column(String, nullable=False, default="/balloons/balloon-1.png")

    # Relações
    room = relationship(
        "Room",
        back_populates="room_problems"
    )

    problem = relationship(
        "Problem",
        back_populates="room_problems"
    )