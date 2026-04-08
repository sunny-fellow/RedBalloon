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
    deleted_at = Column(DateTime, nullable=True)  # NULL = ativo, não-NULL = deletado

    messages = relationship(
        "Message",
        back_populates="user"
    )

    liked_messages = relationship(
        "MessageReact",
        back_populates="user"
    )

    # Problemas
    submissions = relationship(
        "Submission",
        back_populates="user"
    )

    liked_submissions = relationship(
        "SubmissionReact",
        back_populates="user"
    )

    problems_created = relationship(
        "Problem",
        back_populates="creator"
    )

    # Relações entre usuários
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

    # Salas
    room_participations = relationship(
        "RoomParticipant",
        back_populates="user"
    )

    mementos = relationship(
        "Memento",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    problem_reactions = relationship(
        "ProblemReact",
        back_populates="user"
    )
    
    @property
    def is_deleted(self):
        """Propriedade auxiliar para verificar se o usuário está deletado"""
        return self.deleted_at is not None
    
    def soft_delete(self):
        """Método para marcar o usuário como deletado"""
        self.deleted_at = datetime.now(timezone.utc)
    
    def restore(self):
        """Método para restaurar um usuário deletado"""
        self.deleted_at = None