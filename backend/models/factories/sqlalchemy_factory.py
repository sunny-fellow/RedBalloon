from models.factories.repository_factory import RepositoryFactory

# Importa as implementações concretas
from models.user.user_repository_impl import SQLAlchemyUserRepository
from models.problem.problem_repository_impl import SQLAlchemyProblemRepository
from models.submission.submission_repository_impl import SQLAlchemySubmissionRepository
from models.message.message_repository_impl import SQLAlchemyMessageRepository
from models.room.room_repository_impl import SQLAlchemyRoomRepository

# Importa as interfaces para type hint
from models.user.user_repository import UserRepository
from models.problem.problem_repository import ProblemRepository
from models.submission.submission_repository import SubmissionRepository
from models.message.message_repository import MessageRepository
from models.room.room_repository import RoomRepository


class SQLAlchemyRepositoryFactory(RepositoryFactory):
    """Fábrica concreta que cria repositórios com SQLAlchemy"""
    
    def create_user_repository(self) -> UserRepository:
        return SQLAlchemyUserRepository()
    
    def create_problem_repository(self) -> ProblemRepository:
        return SQLAlchemyProblemRepository()
    
    def create_submission_repository(self) -> SubmissionRepository:
        return SQLAlchemySubmissionRepository()
    
    def create_message_repository(self) -> MessageRepository:
        return SQLAlchemyMessageRepository()
    
    def create_room_repository(self) -> RoomRepository:
        return SQLAlchemyRoomRepository()