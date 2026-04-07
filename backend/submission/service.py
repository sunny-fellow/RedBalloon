# submission/service.py (modificado com logger)
from models.factories.sqlalchemy_factory import SQLAlchemyRepositoryFactory
from database.service import DatabaseService
from utils.singleton import Singleton
from utils.app_error import AppError
from utils.adapter.json_logger_adapter import JsonLoggerAdapter
from event_bus import EventBus, Event, EventType
from submission.validators.submit import SubmissionValidator
from execution.service import ExecutionService
from datetime import datetime, timezone
from utils.adapter.logger_factory import LoggerFactory  # Adicionar import

@Singleton
class SubmissionService:
    def __init__(self, logger_type: str = None):
        self.db_service = DatabaseService()
        factory = SQLAlchemyRepositoryFactory()
        self.repository = factory.create_submission_repository()
        self.executor = ExecutionService(self.db_service)
        
        # Criar logger usando a fábrica
        self.logger = LoggerFactory.create_logger(logger_type)
        self.event_bus = EventBus()

    def submit(self, data):
        SubmissionValidator().validate(data)

        user_id = data["user_id"]
        problem_id = data["problem_id"]
        language = data["language"]
        source_code = data["source_code"]

        self.logger.info(
            f"Iniciando submissão de código",
            context={
                "user_id": user_id,
                "problem_id": problem_id,
                "language": language,
                "code_length": len(source_code),
                "action": "submit_start"
            }
        )

        exec_res = self.executor.run(
            problem_id=problem_id,
            source_code=source_code,
            language=language
        )

        status = exec_res.get("status", "JUDGING")
        if status not in ["ACCEPTED", "WRONG_ANSWER", "VERIFICATION_ERROR",
                          "TIME_LIMIT_EXCEEDED", "MEMORY_LIMIT_EXCEEDED",
                          "RUNTIME_ERROR", "COMPILATION_ERROR"]:
            status = "JUDGING"

        def _save(session):
            sub = self.repository.save_submission(
                session=session,
                problem_id=problem_id,
                user_id=user_id,
                code=source_code,
                language=language,
                time_spent=exec_res.get("time_spent", 0),  # Usa 0 se não encontrar o campo,
                status=status,
                submitted_at=datetime.now(timezone.utc).isoformat()
            )
            
            # Log do resultado da submissão
            log_context = {
                "submission_id": sub.submission_id,
                "user_id": user_id,
                "problem_id": problem_id,
                "language": language,
                "status": status,
                "time_spent": exec_res.get("time_spent"),
                "action": "submit_result"
            }
            
            if status == "ACCEPTED":
                self.logger.info(
                    f"Submissão aceita! Problema resolvido com sucesso",
                    context=log_context
                )
            elif status in ["TIME_LIMIT_EXCEEDED", "MEMORY_LIMIT_EXCEEDED"]:
                self.logger.warning(
                    f"Submissão excedeu limites",
                    context=log_context
                )
            elif status in ["COMPILATION_ERROR", "RUNTIME_ERROR"]:
                self.logger.error(
                    f"Submissão falhou com erro de execução",
                    context=log_context
                )
            else:
                self.logger.debug(
                    f"Submissão processada com status: {status}",
                    context=log_context
                )
            self.event_bus.emit(Event(
                type=EventType.SUBMISSION_ACCEPTED,
                payload={
                    "submission_id": sub.submission_id,
                    "user_id": user_id,
                    "problem_id": problem_id,
                    "status": status,
                    "room_id": data.get("room_id"),  # se veio de sala
                    "time_spent": exec_res.get("time_spent")
                }
            ))
            return {
                "submission_id": sub.submission_id,  # <-- Mudança aqui
                "status": status,
                **exec_res
            }

        return self.db_service.run(_save, user_id=user_id)

    def problem_submissions(self, problem_id):
        def _query(session):
            subs = self.repository.get_any_submission(session, problem_id)

            result = []
            for s in subs:
                likes = sum(1 for r in s.reacts if r.reaction.value == "LIKE")
                dislikes = sum(1 for r in s.reacts if r.reaction.value == "DISLIKE")

                result.append({
                    "submission_id": s.submission_id,
                    "problem_id": s.problem_id,
                    "user_id": s.user_id,
                    "user_name": s.user.name,
                    "user_avatar": s.user.avatar,
                    "status": s.status.value,
                    "submitted_at": s.submitted_at,
                    "likes": likes,
                    "dislikes": dislikes,
                    "time_spent": s.time_spent
                })

            result.sort(key=lambda x: x["likes"], reverse=True)
            
            self.logger.debug(
                f"Listagem de submissões aceitas para problema",
                context={
                    "problem_id": problem_id,
                    "submissions_count": len(result),
                    "action": "problem_submissions"
                }
            )
            
            return result

        return self.db_service.run(_query)

    def react(self, data):
        user_id = data["user_id"]
        submission_id = data["submission_id"]
        reaction = data["reaction"].upper()

        if reaction not in ["LIKE", "DISLIKE"]:
            self.logger.warning(
                f"Tipo de reação inválido para submissão",
                context={
                    "user_id": user_id,
                    "submission_id": submission_id,
                    "invalid_reaction": data.get("reaction"),
                    "action": "react_submission"
                }
            )
            raise AppError("Invalid reaction type")

        def _execute(session):
            sub = self.repository.get_submission(session, submission_id)
            if not sub:
                self.logger.warning(
                    f"Tentativa de reagir a submissão inexistente",
                    context={
                        "user_id": user_id,
                        "submission_id": submission_id,
                        "action": "react_submission"
                    }
                )
                raise AppError("Submission not found")

            existing = self.repository.get_existing_react(session, submission_id, user_id)

            if existing:
                if existing.reaction.value == reaction:
                    self.repository.remove_react(session, existing)
                    
                    self.logger.info(
                        f"Reação removida da submissão",
                        context={
                            "submission_id": submission_id,
                            "user_id": user_id,
                            "reaction": reaction,
                            "action_type": "REMOVED",
                            "action": "react_submission"
                        }
                    )
                    return {"status": "REMOVED"}
                else:
                    self.repository.update_react(existing, reaction)
                    
                    self.logger.info(
                        f"Reação atualizada na submissão",
                        context={
                            "submission_id": submission_id,
                            "user_id": user_id,
                            "old_reaction": existing.reaction.value,
                            "new_reaction": reaction,
                            "action_type": "UPDATED",
                            "action": "react_submission"
                        }
                    )
                    return {"status": "UPDATED"}

            self.repository.add_react(session, submission_id, user_id, reaction)
            
            self.logger.info(
                f"Nova reação adicionada à submissão",
                context={
                    "submission_id": submission_id,
                    "user_id": user_id,
                    "reaction": reaction,
                    "action_type": "CREATED",
                    "action": "react_submission"
                }
            )
            
            return {"status": "CREATED"}

        return self.db_service.run(_execute)
    
    def details(self, data):
        submission_id = data["submission_id"]
        user_id = data["user_id"]

        def _query(session):
            details = self.repository.get_submission_details(session, submission_id, user_id)
            if not details:
                self.logger.warning(
                    f"Tentativa de acessar detalhes de submissão inexistente",
                    context={
                        "submission_id": submission_id,
                        "user_id": user_id,
                        "action": "submission_details"
                    }
                )
                raise AppError("Submission not found", 404)
            
            self.logger.info(
                f"Detalhes da submissão acessados",
                context={
                    "submission_id": submission_id,
                    "user_id": user_id,
                    "problem_id": details.get("problem_id"),
                    "status": details.get("status"),
                    "action": "submission_details"
                }
            )
            
            return details

        return self.db_service.run(_query, user_id=user_id)