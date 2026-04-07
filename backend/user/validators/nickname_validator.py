import re

from utils.app_error import AppError
from utils.interfaces.validator import Validator

class NicknameValidator(Validator):
    """
    Validador para campo nickname de usuário.
    Verifica se o nickname não está vazio, tem no máximo 12 caracteres
    e não contém números.
    """
    @staticmethod
    def validate(nickname: str):
        if not nickname or not nickname.strip():
            raise AppError("O campo 'nickname' não pode ser vazio.")

        if len(nickname) > 12:
            raise AppError("O 'nickname' deve ter no máximo 12 caracteres.")

        if re.search(r"\d", nickname):
            raise AppError("O 'nickname' não pode conter números.")