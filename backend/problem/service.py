from database.service import DatabaseService
from utils.singleton import Singleton
from utils.app_error import AppError
from problem.repository import ProblemRepository

from models.problem.problem import Problem
from models.problem.problem_test_case import ProblemTestCase
from models.problem.problem_input import ProblemInput
from models.problem.problem_checker import ProblemChecker
from models.enums import ValidationMode, ReactionType

from problem.validators.create_problem import CreateProblemValidator


@Singleton
class ProblemService:

    def __init__(self):
        self.db_service = DatabaseService()
        self.repository = ProblemRepository()

    # ---------------- CREATE ----------------
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

            # -------- INPUTS + OUTPUTS --------
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

            # -------- CHECKER --------
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
                session.flush()  # IMPORTANTE

                for inp in inputs:
                    session.add(
                        ProblemInput(
                            problem_id=problem.problem_id,
                            input_data=inp,
                            checker_id=checker.checker_id
                        )
                    )

            # -------- NO VALIDATION --------
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

            return {"problem_id": problem.problem_id}

        return self.db_service.run(func, data["creator_id"])

    # ---------------- LIST ----------------
    def list(self, data):

        def func(session):

            problems = self.repository.list_problems(
                session=session,
                query=data.get("query"),
                tags=data.get("tags")
            )

            if not problems:
                return []

            ids = [p.problem_id for p in problems]

            reactions = self.repository.get_reactions_count(session, ids)
            submissions = self.repository.get_submission_stats(session, ids)
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

            return result

        return self.db_service.run(func)
    
    def problem_info(self, data):
        problem_id = data["problem_id"]
        user_id = data["user_id"]

        def func(session):

            problem = self.repository.get_problem_by_id(session, problem_id)

            if not problem:
                raise AppError("Problema não encontrado", 404)

            creator_name = self.repository.get_creator_name(
                session, problem.creator_id
            )

            reactions = self.repository.get_reactions(session, problem_id)

            submissions = self.repository.get_submission_stats(
                session, problem_id
            )

            tags = self.repository.get_problem_tags(session, problem_id)

            comments = self.repository.get_comments(session, problem_id)

            reaction = self.repository.get_user_reaction(session, problem_id, user_id)

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
                raise AppError("Tipo de reação inválido", 400)

            # opcional (recomendado): validar se problema existe
            problem = self.repository.get_problem_by_id(session, problem_id)
            if not problem:
                raise AppError("Problema não encontrado", 404)

            action = self.repository.upsert_problem_react(
                session,
                problem_id,
                user_id,
                react_type
            )

            return {
                "action": action  # created | updated | removed
            }

        return self.db_service.run(func)
    
    def count_problems(self):

        def func(session):
            return self.repository.count_problems(session)

        return self.db_service.run(func)