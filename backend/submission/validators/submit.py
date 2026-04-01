from utils.validator import Validator
from utils.app_error import AppError

class SubmissionValidator(Validator):
    @staticmethod  # ADICIONE ESTE DECORADOR
    def validate(data):  # Mantém o parâmetro data
        user_id = data.get("user_id")
        problem_id = data.get("problem_id")
        source_code = data.get("source_code")
        language = data.get("language")

        if not user_id:
            raise AppError("ID do usuário é um campo obrigatório")
        
        if not problem_id:
            raise AppError("ID do problema é um campo obrigatório")
        
        if language not in ["C", "CPP", "JAVA", "PYTHON"]:
            raise AppError("Linguagem do código inválida ou não informada")
        
        if not source_code:
            raise AppError("Código desenvolvido pelo usuário é obrigatório")
        
        if language == "JAVA" and "public class Solution" not in source_code:
            raise AppError("Códigos em java devem implementar a classe Solution")