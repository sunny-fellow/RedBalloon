# listeners/statistics_listener.py
from event_bus import EventListener, Event, EventType
from models.factories.sqlalchemy_factory import SQLAlchemyRepositoryFactory
from database.service import DatabaseService
from utils.adapter.json_logger_adapter import JsonLoggerAdapter

class StatisticsListener(EventListener):
    """Atualiza estatísticas de problemas quando uma submissão é aceita"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        factory = SQLAlchemyRepositoryFactory()
        self.problem_repo = factory.create_problem_repository()
        self.logger = JsonLoggerAdapter("logs", "statistics_events.json")
    
    def handle(self, event: Event):
        if event.type == EventType.SUBMISSION_ACCEPTED:
            problem_id = event.payload["problem_id"]
            user_id = event.payload["user_id"]
            
            def func(session):
                # Incrementa o contador de solved_count no problema
                problem = self.problem_repo.get_problem_by_id(session, problem_id)
                if problem:
                    problem.solved_count = (problem.solved_count or 0) + 1
                    session.flush()
                    
                    self.logger.info(
                        f"Estatísticas do problema atualizadas",
                        context={
                            "problem_id": problem_id,
                            "user_id": user_id,
                            "new_solved_count": problem.solved_count,
                            "action": "update_statistics"
                        }
                    )
            
            self.db_service.run(func)