from database.service import DatabaseService
from utils.singleton import Singleton
from utils.validation_error import ValidationError
from problem.repository import ProblemRepository

from models.problem.problem import Problem
from models.problem.problem_test_case import ProblemTestCase
from models.problem.problem_input import ProblemInput
from models.problem.problem_input import ProblemInput
from models.problem.problem_checker import ProblemChecker
from models.enums import ValidationMode

@Singleton
class ProblemService:

    def __init__(self):
        self.db_service = DatabaseService()
        self.repository = ProblemRepository()

    def create_problem(self, data):
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
            session.flush()  # gera problem_id

            # -------- INPUTS + OUTPUTS --------

            if validation_mode == ValidationMode.INPUTS_OUTPUTS:

                cases = data.get("inputs_outputs")

                if not cases:
                    raise ValidationError(
                        "inputs_outputs é obrigatório para INPUTS_OUTPUTS"
                    )

                for case in cases:

                    test_case = ProblemTestCase(
                        problem_id=problem.problem_id,
                        input_data=case["input"],
                        output_data=case["output"]
                    )

                    session.add(test_case)

            # -------- CHECKER --------

            elif validation_mode == ValidationMode.CHECKER_ALGORITHM:

                checker_data = data.get("checker")
                inputs = data.get("inputs")

                if not checker_data:
                    raise ValidationError(
                        "checker é obrigatório para CHECKER_ALGORITHM"
                    )

                if not inputs:
                    raise ValidationError(
                        "inputs é obrigatório para CHECKER_ALGORITHM"
                    )

                checker = ProblemChecker(
                    problem_id=problem.problem_id,
                    language=checker_data["language"],
                    source_code=checker_data["source_code"]
                )

                session.add(checker)

                for inp in inputs:

                    session.add(
                        ProblemInput(
                            problem_id=problem.problem_id,
                            input_data=inp,
                            checker_id = checker.checker_id
                        )
                    )

            # -------- NO VALIDATION --------

            elif validation_mode == ValidationMode.NO_VALIDATION:

                inputs = data.get("inputs")

                if not inputs:
                    raise ValidationError(
                        "inputs é obrigatório para NO_VALIDATION"
                    )

                for inp in inputs:

                    session.add(
                        ProblemInput(
                            problem_id=problem.problem_id,
                            input_data=inp
                        )
                    )

            return {"problem_id": problem.problem_id}

        return self.db_service.run(func)
