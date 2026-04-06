from utils.interfaces.validator import Validator
from utils.app_error import AppError
from models.enums import MessageTags

class GetCommentsValidator(Validator):
    @staticmethod
    def validate(data):
        context_type = data.get("context_type")
        if context_type not in ["GLOBAL", "PROBLEM", "SOLUTION"]:
            raise AppError("context_type inválido. Deve ser 'GLOBAL', 'PROBLEM' ou 'SOLUTION'", 400)

        if context_type in ["PROBLEM", "SOLUTION"]:
            if "context_ref_id" not in data or not isinstance(data["context_ref_id"], int):
                raise AppError("context_ref_id é obrigatório e deve ser inteiro para PROBLEM ou SOLUTION", 400)

        query = data.get("query")
        if query is not None and not isinstance(query, str):
            raise AppError("query deve ser uma string", 400)

        tags = data.get("tags")
        if tags is not None:
            if not isinstance(tags, list):
                raise AppError("tags deve ser uma lista de strings", 400)

            invalid_tags = [t for t in tags if t not in [tag.value for tag in MessageTags]]
            if invalid_tags:
                raise AppError(f"tags inválidas: {invalid_tags}. Valores permitidos: {[tag.value for tag in MessageTags]}", 400)