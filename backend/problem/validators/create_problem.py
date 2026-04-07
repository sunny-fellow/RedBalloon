from utils.interfaces.validator import Validator
from utils.app_error import AppError

class CreateProblemValidator(Validator):
    """
    Validador para dados de criação de problema.
    Responsável por validar todos os campos fornecidos na criação de um novo problema,
    incluindo limites e validação específica por modo de validação.
    """
    MAX_TIME = 5000 # em ms
    MAX_MEMORY = 700 # em MB

    @staticmethod
    def validate(data: dict):
        required_fields = ["creator_id", "title", "description", "time_limit",
                           "memory_limit", "validation_mode", "difficulty"]

        for field in required_fields:
            if field not in data or data[field] is None:
                raise AppError(f"{field} é obrigatório")

        time_limit = data["time_limit"]
        memory_limit = data["memory_limit"]

        if time_limit <= 0 or time_limit > CreateProblemValidator.MAX_TIME:
            raise AppError(
                f"time_limit deve estar entre 1 e {CreateProblemValidator.MAX_TIME} ms"
            )

        if memory_limit <= 0 or memory_limit > CreateProblemValidator.MAX_MEMORY:
            raise AppError(f"memory_limit deve estar entre 1 e {CreateProblemValidator.MAX_MEMORY} MB")

        mode = data["validation_mode"]

        if mode == "INPUTS_OUTPUTS":
            ios = data.get("inputs_outputs")

            if not ios or len(ios) == 0:
                raise AppError("inputs_outputs é obrigatório para INPUTS_OUTPUTS")

            for i, item in enumerate(ios):
                if "input" not in item or "output" not in item:
                    raise AppError(f"inputs_outputs[{i}] inválido")

        elif mode == "CHECKER_ALGORITHM":
            checker = data.get("checker")
            inputs = data.get("inputs")

            if not checker:
                raise AppError("checker é obrigatório para CHECKER_ALGORITHM")

            if not inputs or len(inputs) == 0:
                raise AppError("inputs é obrigatório para CHECKER_ALGORITHM")

            if "language" not in checker or "source_code" not in checker:
                raise AppError("checker inválido")

        elif mode == "NO_VALIDATION":
            pass

        else:
            raise AppError("validation_mode inválido")