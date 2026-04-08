from abc import ABC, abstractmethod

# Importa todas as interfaces dos repositórios
from models.user.user_repository import UserRepository
from models.problem.problem_repository import ProblemRepository
from models.submission.submission_repository import SubmissionRepository
from models.message.message_repository import MessageRepository
from models.room.room_repository import RoomRepository

class RepositoryFactory(ABC):
    """
    Abstract Factory para criação de repositórios
    """
    @abstractmethod
    def create_user_repository(self) -> UserRepository:
        """
        Cria um repositório de usuários
        """
        pass
    
    @abstractmethod
    def create_problem_repository(self) -> ProblemRepository:
        """
        Cria um repositório de problemas
        """
        pass
    
    @abstractmethod
    def create_submission_repository(self) -> SubmissionRepository:
        """
        Cria um repositório de submissões
        """
        pass
    
    @abstractmethod
    def create_message_repository(self) -> MessageRepository:
        """
        Cria um repositório de mensagens
        """
        pass
    
    @abstractmethod
    def create_room_repository(self) -> RoomRepository:
        """
        Cria um repositório de salas
        """
        pass