from utils.app_error import AppError
from models.enums import MessageTags

class CommentValidator:

    @staticmethod
    def validate(data):
        context_type = data.get("context_type")
        context_ref_id = data.get("context_ref_id")
        parent_message = data.get("parent_message")
        user_id = data.get("user_id")
        message = data.get("message")

        # context_type
        if not context_type:
            raise AppError("context_type é obrigatório", 400)
        if context_type not in ["GLOBAL", "PROBLEM", "SOLUTION"]:
            raise AppError("context_type inválido", 400)

        # context_ref_id obrigatório se context_type não for GLOBAL
        if context_type in ["PROBLEM", "SOLUTION"]:
            if context_ref_id is None:
                raise AppError(f"context_ref_id é obrigatório para {context_type}", 400)
            if not isinstance(context_ref_id, int) or context_ref_id <= 0:
                raise AppError("context_ref_id inválido", 400)

        # parent_message opcional
        if parent_message is not None:
            if not isinstance(parent_message, int) or parent_message <= 0:
                raise AppError("parent_message inválido", 400)

        # user_id
        if not user_id or not isinstance(user_id, int) or user_id <= 0:
            raise AppError("user_id inválido", 400)

        # message
        if not message or not isinstance(message, str) or not message.strip():
            raise AppError("message é obrigatório e não pode ser vazio", 400)
        
        # tags
        tags = data.get("tags")
        if tags is not None:
            if not isinstance(tags, list):
                raise AppError("tags deve ser uma lista de strings", 400)

            invalid_tags = [t for t in tags if t not in [tag.value for tag in MessageTags]]
            if invalid_tags:
                raise AppError(f"tags inválidas: {invalid_tags}. Valores permitidos: {[tag.value for tag in MessageTags]}", 400)