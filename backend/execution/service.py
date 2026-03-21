from typing import List
from utils.singleton import Singleton

from models import Problem, ProblemTestCase, ProblemChecker
from models.enums import ValidationMode
from database.service import DatabaseService
from execution.executor_factory import ExecutorFactory

@Singleton
class ExecutionService:

    def __init__(self, db: DatabaseService):
        self.db = db

    def run(
        self,
        problem_id: int,
        source_code: str,
        language: str
    ):
        def _execute(session):
            problem: Problem = session.get(Problem, problem_id)

            if not problem:
                raise Exception("Problem not found")

            executor = ExecutorFactory.get_executor(language)
            validation_mode = problem.validation_mode

            if validation_mode == ValidationMode.NO_VALIDATION:
                return {"status": "ACCEPTED"}

            if validation_mode == ValidationMode.INPUTS_OUTPUTS:
                return self._run_test_cases(executor, source_code, problem)

            if validation_mode == ValidationMode.CHECKER_ALGORITHM:
                return self._run_checker(executor, source_code, problem)

            raise Exception("Invalid validation mode")

        return self.db.run(_execute)

    # =========================
    # TEST CASES
    # =========================
    def _run_test_cases(self, executor, source_code, problem: Problem):
        media_tempo_gasto = 0

        for test in problem.test_cases:
            res = executor.execute(
                source_code,
                test.input_data,
                problem.time_limit,
                problem.memory_limit
            )

            # se houve erro de execução, retorna imediatamente
            if res["status"] != "ACCEPTED":
                return {
                    "input": test.input_data,
                    "status": res["status"],
                    "error": res.get("error")
                }

            output = res.get("output", "").strip()
            expected = test.output_data.strip()

            if output != expected:
                return {
                    "input": test.input_data,
                    "status": "WRONG_ANSWER",
                    "output": output
                }
            
            media_tempo_gasto += res.time_spent_ms

        # se passou em todos os testes
        media_tempo_gasto //= len(problem.test_cases)
        return {"status": "ACCEPTED", "time_spent": media_tempo_gasto}

    # =========================
    # CHECKER
    # =========================
    def _run_checker(self, executor, source_code, problem: Problem):
        checker: ProblemChecker = problem.checker

        if not checker:
            raise Exception("Checker not found")

        checker_executor = ExecutorFactory.get_executor(checker.language)
        media_tempo_gasto = 0

        for test in problem.test_cases:
            user_res = executor.execute(
                source_code,
                test.input_data,
                problem.time_limit,
                problem.memory_limit
            )

            # erro do usuário
            if user_res["status"] != "ACCEPTED":
                return {
                    "input": test.input_data,
                    "status": user_res["status"],
                    "error": user_res.get("error")
                }

            user_output = user_res.get("output", "").strip()

            # roda checker
            checker_input = f"{test.input_data}\n{user_output}"
            checker_res = checker_executor.execute(
                checker.source_code,
                checker_input,
                problem.time_limit,
            )

            # erro no checker
            if checker_res["status"] != "ACCEPTED":
                return {
                    "input": test.input_data,
                    "status": "VERIFICATION_ERROR",
                    "checker_error": checker_res.get("error")
                }

            checker_output = checker_res.get("output", "").strip().lower()
            if checker_output not in ["1", "true"]:
                return {
                    "input": test.input_data,
                    "status": "WRONG_ANSWER",
                    "user_output": user_output,
                    "checker_output": checker_output
                }
            
            media_tempo_gasto += user_res.time_spent_ms

        # se passou em todos os testes/checkers
        media_tempo_gasto //= len(problem.test_cases)
        return {"status": "ACCEPTED", "time_spent": media_tempo_gasto}