from datetime import datetime

from utils.app_error import AppError
from utils.singleton import Singleton

# Services
from user.service import UserService
from problem.service import ProblemService

# User Commands
from user.commands.delete_user import DeleteUserCommand
from user.commands.list_users import ListUsersCommand
from user.commands.update_user import UpdateUserCommand
from user.commands.user_details import UserDetailsCommand
from user.commands.user_follow import UserFollowCommand

# Problem Commands
from problem.commands.create_problem import CreateProblemCommand
from problem.commands.list_problems import ListProblemsCommand
from problem.commands.problem_info import ProblemInfoCommand
from problem.commands.problem_react import ProblemReactCommand

from utils.reports.report_factory import ReportFactory, ReportType

from utils.adapter.logger_factory import LoggerFactory
from message.service import MessageService
from room.service import RoomService
from submission.service import SubmissionService
import os

@Singleton
class FacadeSingletonController:
    def __init__(self):
        # Definir tipo de logger baseado no ambiente
        env = os.getenv("ENV", "development")
        
        if env == "development":
            logger_type = "console"  # Console em desenvolvimento
        
        elif env == "production":
            logger_type = "json"     # JSON em produção
        
        else:
            logger_type = "console"  # Fallback
        
        # Criar serviços com o logger configurado
        self.user_service = UserService(logger_type=logger_type)
        self.problem_service = ProblemService(logger_type=logger_type)
        self.message_service = MessageService(logger_type=logger_type)
        self.room_service = RoomService(logger_type=logger_type)
        self.submission_service = SubmissionService(logger_type=logger_type)

    # USER
    def list_users(self, query=None, country=None):
        command = ListUsersCommand(
            self.user_service,
            {"query": query, "country": country}
        )
        return command.execute()

    def user_details(self, user_id, requester_id):
        print("FACADE: user_details START")
        print(f"FACADE: user_id={user_id}, requester_id={requester_id}")

        command = UserDetailsCommand(
            self.user_service,
            {
                "user_id": user_id,
                "requester_id": requester_id
            }
        )
        result = command.execute()
        return result

    def follow_user(self, follower_id, following_id):
        command = UserFollowCommand(
            self.user_service,
            {
                "follower_id": follower_id,
                "following_id": following_id
            }
        )
        return command.execute()

    def update_user(self, user_id, data):
        command = UpdateUserCommand(self.user_service, user_id, data)
        return command.execute()

    def delete_user(self, user_id):
        command = DeleteUserCommand(self.user_service, user_id)
        return command.execute()

    # PROBLEM
    def create_problem(self, data):
        command = CreateProblemCommand(self.problem_service, data)
        return command.execute()

    def list_problems(self, query=None, tags=None):
        command = ListProblemsCommand(
            self.problem_service,
            {
                "query": query,
                "tags": tags
            }
        )
        return command.execute()

    def problem_info(self, problem_id, user_id):
        command = ProblemInfoCommand(
            self.problem_service,
            {
                "problem_id": problem_id,
                "user_id": user_id
            }
        )
        return command.execute()

    def react_problem(self, data):
        command = ProblemReactCommand(self.problem_service, data)
        return command.execute()

    def count_users(self):
        return self.user_service.count_users()

    def count_problems(self):
        return self.problem_service.count_problems()
    
    def generate_access_report(self, start_date: datetime, end_date: datetime, format_type: str):
        """Gera relatório de estatísticas de acesso"""
        if format_type == "html":
            report = ReportFactory.create_report(ReportType.HTML)
        elif format_type == "pdf":
            report = ReportFactory.create_report(ReportType.PDF)
        else:
            raise AppError(f"Formato de relatório inválido: {format_type}", 400)
        
        return report.generate(start_date, end_date)