from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    nickname = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    avatar = Column(String)
    description = Column(String)
    nationality = Column(String)
    created_at = Column(String, default=lambda: datetime.now(timezone.utc).isoformat())


    # -------- mensagens --------

    messages = relationship(
        "Message",
        back_populates="user",
        cascade="all, delete"
    )

    liked_messages = relationship(
        "MessageReact",
        back_populates="user",
        cascade="all, delete"
    )


    # -------- problemas --------

    submissions = relationship(
        "Submission",
        back_populates="user",
        cascade="all, delete"
    )

    liked_submissions = relationship(
        "SubmissionReact",
        back_populates="user",
        cascade="all, delete"
    )

    problems_created = relationship(
        "Problem",
        back_populates="creator",
        cascade="all, delete"
    )


    # -------- relações entre usuários --------

    followers = relationship(
        "UserFollow",
        foreign_keys="UserFollow.following_id",
        back_populates="following"
    )

    followings = relationship(
        "UserFollow",
        foreign_keys="UserFollow.follower_id",
        back_populates="follower"
    )


    # -------- salas --------

    room_participations = relationship(
        "RoomParticipant",
        back_populates="user",
        cascade="all, delete"
    )

    # ------- mementos ------
    mementos = relationship(
        "Memento",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    problem_reactions = relationship(
        "ProblemReact",
        back_populates="user",
        cascade="all, delete"
    )