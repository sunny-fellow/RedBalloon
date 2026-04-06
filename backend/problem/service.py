from models.factories.sqlalchemy_factory import SQLAlchemyRepositoryFactory
from database.service import DatabaseService
from utils.singleton import Singleton
from utils.app_error import AppError
from utils.adapter.json_logger_adapter import JsonLoggerAdapter

from models.problem.problem import Problem
from models.problem.problem_test_case import ProblemTestCase
from models.problem.problem_input import ProblemInput
from models.problem.problem_checker import ProblemChecker
from models.enums import ValidationMode, ReactionType

from problem.validators.create_problem import CreateProblemValidator
from utils.adapter.logger_factory import LoggerFactory  # <-- ADICIONAR ESTA LINHA

@Singleton
class ProblemService:
    def __init__(self, logger_type: str = None):
        self.db_service = DatabaseService()
        factory = SQLAlchemyRepositoryFactory()
        self.repository = factory.create_problem_repository()
        
        # Adapter para JSON logs
        self.logger = LoggerFactory.create_logger(logger_type)

    # CREATE
    def create_problem(self, data):
        CreateProblemValidator.validate(data)
        validation_mode = ValidationMode(data["validation_mode"])

        def func(session):
            problem = Problem(
                creator_id=data["creator_id"],
                title=data["title"],
                description=data["description"],
                time_limit=data["time_limit"],
                memory_limit=data["memory_limit"],
                validation_mode=validation_mode,
                difficulty=data["difficulty"],
                private=data.get("private", False)
            )

            session.add(problem)
            session.flush()

            # INPUTS + OUTPUTS
            if validation_mode == ValidationMode.INPUTS_OUTPUTS:
                cases = data.get("inputs_outputs")

                if not cases:
                    raise AppError(
                        "inputs_outputs é obrigatório para INPUTS_OUTPUTS"
                    )

                for case in cases:
                    session.add(
                        ProblemTestCase(
                            problem_id=problem.problem_id,
                            input_data=case["input"],
                            output_data=case["output"]
                        )
                    )
                
                self.logger.info(
                    f"Problema criado com casos de teste",
                    context={
                        "problem_id": problem.problem_id,
                        "creator_id": data["creator_id"],
                        "title": data["title"],
                        "validation_mode": "INPUTS_OUTPUTS",
                        "test_cases_count": len(cases),
                        "action": "create_problem"
                    }
                )

            # CHECKER
            elif validation_mode == ValidationMode.CHECKER_ALGORITHM:
                checker_data = data.get("checker")
                inputs = data.get("inputs")

                if not checker_data:
                    raise AppError("checker é obrigatório")

                if not inputs:
                    raise AppError("inputs é obrigatório")

                checker = ProblemChecker(
                    problem_id=problem.problem_id,
                    language=checker_data["language"],
                    source_code=checker_data["source_code"]
                )

                session.add(checker)
                session.flush()

                for inp in inputs:
                    session.add(
                        ProblemInput(
                            problem_id=problem.problem_id,
                            input_data=inp,
                            checker_id=checker.checker_id
                        )
                    )
                
                self.logger.info(
                    f"Problema criado com checker algorithm",
                    context={
                        "problem_id": problem.problem_id,
                        "creator_id": data["creator_id"],
                        "title": data["title"],
                        "validation_mode": "CHECKER_ALGORITHM",
                        "checker_language": checker_data["language"],
                        "inputs_count": len(inputs),
                        "action": "create_problem"
                    }
                )

            # NO VALIDATION
            elif validation_mode == ValidationMode.NO_VALIDATION:
                inputs = data.get("inputs")

                if not inputs:
                    raise AppError("inputs é obrigatório")

                for inp in inputs:
                    session.add(
                        ProblemInput(
                            problem_id=problem.problem_id,
                            input_data=inp
                        )
                    )
                
                self.logger.info(
                    f"Problema criado sem validação",
                    context={
                        "problem_id": problem.problem_id,
                        "creator_id": data["creator_id"],
                        "title": data["title"],
                        "validation_mode": "NO_VALIDATION",
                        "inputs_count": len(inputs),
                        "action": "create_problem"
                    }
                )

            return {"problem_id": problem.problem_id}

        return self.db_service.run(func, data["creator_id"])

    # LIST
    def list(self, data):
        def func(session):
            problems = self.repository.list_problems(
                session=session,
                query=data.get("query"),
                tags=data.get("tags")
            )

            if not problems:
                self.logger.debug(
                    f"Listagem de problemas retornou vazia",
                    context={
                        "query": data.get("query"),
                        "tags": data.get("tags"),
                        "action": "list_problems"
                    }
                )
                return []

            ids = [p.problem_id for p in problems]

            reactions = self.repository.get_reactions_count(session, ids)
            submissions = self.repository.get_submission_stats_bulk(session, ids)
            tags = self.repository.get_tags(session, ids)

            result = []

            for p in problems:
                result.append({
                    "problem_id": p.problem_id,
                    "title": p.title,
                    "description": p.description,
                    "difficulty": p.difficulty,
                    "created_at": p.created_at,
                    "likes": reactions[p.problem_id]["likes"],
                    "dislikes": reactions[p.problem_id]["dislikes"],
                    "total_submissions": submissions[p.problem_id]["total"],
                    "accepted_submissions": submissions[p.problem_id]["accepted"],
                    "tags": tags[p.problem_id]
                })

            self.logger.debug(
                f"Listagem de problemas realizada",
                context={
                    "query": data.get("query"),
                    "tags": data.get("tags"),
                    "result_count": len(result),
                    "action": "list_problems"
                }
            )

            return result

        return self.db_service.run(func)
    
    def problem_info(self, data):
        problem_id = data["problem_id"]
        user_id = data["user_id"]

        def func(session):
            problem = self.repository.get_problem_by_id(session, problem_id)

            if not problem:
                self.logger.warning(
                    f"Tentativa de acesso a problema inexistente",
                    context={
                        "problem_id": problem_id,
                        "user_id": user_id,
                        "action": "problem_info"
                    }
                )
                raise AppError("Problema não encontrado", 404)

            creator_name = self.repository.get_creator_name(
                session, problem.creator_id
            )

            reactions = self.repository.get_reactions(session, problem_id)

            submissions = self.repository.get_submission_stats_single(
                session, problem_id
            )

            tags = self.repository.get_problem_tags(session, problem_id)

            comments = self.repository.get_comments(session, problem_id)

            reaction = self.repository.get_user_reaction(session, problem_id, user_id)

            self.logger.info(
                f"Problema acessado",
                context={
                    "problem_id": problem_id,
                    "user_id": user_id,
                    "title": problem.title,
                    "difficulty": problem.difficulty,
                    "action": "view_problem"
                }
            )

            return {
                "problem_id": problem.problem_id,
                "title": problem.title,
                "description": problem.description,
                "time_limit": problem.time_limit,
                "memory_limit": problem.memory_limit,
                "difficulty": problem.difficulty,
                "created_at": problem.created_at,

                "creator_name": creator_name,

                "tags": tags,

                "likes": reactions["likes"],
                "dislikes": reactions["dislikes"],

                "total_submissions": submissions["total"],
                "accepted_submissions": submissions["accepted"],

                "comments": comments,
                "reaction": reaction
            }

        return self.db_service.run(func)
    
    def problem_react(self, data):
        def func(session):

            problem_id = data["problem_id"]
            user_id = data["user_id"]

            try:
                react_type = ReactionType(data["react_type"])
            
            except ValueError:
                self.logger.error(
                    f"Tipo de reação inválido",
                    context={
                        "problem_id": problem_id,
                        "user_id": user_id,
                        "invalid_type": data.get("react_type"),
                        "action": "problem_react"
                    }
                )
                raise AppError("Tipo de reação inválido", 400)

            # Validar se problema existe
            problem = self.repository.get_problem_by_id(session, problem_id)
            if not problem:
                self.logger.warning(
                    f"Tentativa de reagir a problema inexistente",
                    context={
                        "problem_id": problem_id,
                        "user_id": user_id,
                        "react_type": react_type.value,
                        "action": "problem_react"
                    }
                )
                raise AppError("Problema não encontrado", 404)

            action = self.repository.upsert_problem_react(
                session,
                problem_id,
                user_id,
                react_type
            )
            
            self.logger.info(
                f"Reação em problema realizada",
                context={
                    "problem_id": problem_id,
                    "user_id": user_id,
                    "react_type": react_type.value,
                    "action_type": action,  # created, updated, removed
                    "action": "problem_react"
                }
            )
            
            return {
                "action": action
            }

        return self.db_service.run(func)
    
    def count_problems(self):
        def func(session):
            count = self.repository.count_problems(session)
            
            self.logger.debug(
                f"Contagem de problemas realizada",
                context={
                    "total_problems": count,
                    "action": "count_problems"
                }
            )
            
            return count

        return self.db_service.run(func)