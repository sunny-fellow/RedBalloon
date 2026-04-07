from typing import List
from utils.singleton import Singleton

from models import Problem, ProblemChecker
from models.enums import ValidationMode
from database.service import DatabaseService
from execution.execution_context import ExecutionContext

@Singleton
class ExecutionService:
    def __init__(self, db: DatabaseService):
        self.db = db
        self.execution_context = ExecutionContext()  # Contexto compartilhado

    def run(self, problem_id: int, source_code: str, language: str):
        def _execute(session):
            problem: Problem = session.get(Problem, problem_id)

            if not problem:
                raise Exception("Problem not found")

            # Define a estratégia baseada na linguagem
            self.execution_context.set_strategy(language)
            validation_mode = problem.validation_mode

            if validation_mode == ValidationMode.NO_VALIDATION:
                return {"status": "ACCEPTED"}

            if validation_mode == ValidationMode.INPUTS_OUTPUTS:
                return self._run_test_cases(source_code, problem)

            if validation_mode == ValidationMode.CHECKER_ALGORITHM:
                return self._run_checker(source_code, problem)

            raise Exception("Invalid validation mode")

        return self.db.run(_execute)

    def _run_test_cases(self, source_code, problem: Problem):
        media_tempo_gasto = 0

        for test in problem.test_cases:
            res = self.execution_context.execute(
                source_code,
                test.input_data,
                problem.time_limit,
                problem.memory_limit
            )
            
            # Se houve erro de execução, retorna imediatamente
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
            
            media_tempo_gasto += res.get("time_spent_ms", 0)

        # Se passou em todos os testes
        if problem.test_cases:
            media_tempo_gasto //= len(problem.test_cases)
        
        return {"status": "ACCEPTED", "time_spent": media_tempo_gasto}

    def _run_checker(self, source_code, problem: Problem):
        checker: ProblemChecker = problem.checker

        if not checker:
            raise Exception("Checker not found")

        # Contexto separado para o checker
        checker_context = ExecutionContext()
        checker_context.set_strategy(checker.language)
        
        media_tempo_gasto = 0

        for test in problem.test_cases:
            user_res = self.execution_context.execute(
                source_code,
                test.input_data,
                problem.time_limit,
                problem.memory_limit
            )

            # Erro do usuário
            if user_res["status"] != "ACCEPTED":
                return {
                    "input": test.input_data,
                    "status": user_res["status"],
                    "error": user_res.get("error")
                }

            user_output = user_res.get("output", "").strip()

            # Roda checker usando seu próprio contexto
            checker_input = f"{test.input_data}\n{user_output}"
            checker_res = checker_context.execute(
                checker.source_code,
                checker_input,
                problem.time_limit,
                problem.memory_limit  # Adicionado memory_limit que estava faltando
            )

            # Erro no checker
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
            
            media_tempo_gasto += user_res.get("time_spent_ms", 0)

        # Se passou em todos os testes/checkers
        if problem.test_cases:
            media_tempo_gasto //= len(problem.test_cases)
        
        return {"status": "ACCEPTED", "time_spent": media_tempo_gasto}