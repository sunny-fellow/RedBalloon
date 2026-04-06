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

    # Mensagens - REMOVA o cascade="all, delete" para evitar exclusão física
    messages = relationship(
        "Message",
        back_populates="user"
        # cascade removido - não queremos excluir fisicamente
    )

    liked_messages = relationship(
        "MessageReact",
        back_populates="user"
        # cascade removido
    )

    # Problemas
    submissions = relationship(
        "Submission",
        back_populates="user"
        # cascade removido
    )

    liked_submissions = relationship(
        "SubmissionReact",
        back_populates="user"
        # cascade removido
    )

    problems_created = relationship(
        "Problem",
        back_populates="creator"
        # cascade removido
    )

    # Relações entre usuários
    followers = relationship(
        "UserFollow",
        foreign_keys="UserFollow.following_id",
        back_populates="following"
        # cascade removido
    )

    followings = relationship(
        "UserFollow",
        foreign_keys="UserFollow.follower_id",
        back_populates="follower"
        # cascade removido
    )

    # Salas
    room_participations = relationship(
        "RoomParticipant",
        back_populates="user"
        # cascade removido
    )

    # Mementos - mantenha o cascade="all, delete-orphan" se quiser exclusão automática
    mementos = relationship(
        "Memento",
        back_populates="user",
        cascade="all, delete-orphan"  # Este pode manter para limpeza automática
    )

    problem_reactions = relationship(
        "ProblemReact",
        back_populates="user"
        # cascade removido
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