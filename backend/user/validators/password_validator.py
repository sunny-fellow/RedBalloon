import re

from utils.app_error import AppError
from utils.interfaces.validator import Validator

class PasswordValidator(Validator):
    """
    Validador para campo de senha de usuário.
    Verifica se a senha tem entre 8 e 128 caracteres e contém
    pelo menos 3 dos 4 tipos de caracteres: maiúsculas, minúsculas,
    números e caracteres especiais.
    """
    @staticmethod
    def validate(password: str):
        if not password:
            raise AppError("O campo 'password' não pode ser vazio.")

        if len(password) < 8 or len(password) > 128:
            raise AppError("A 'senha' deve ter entre 8 e 128 caracteres.")

        has_upper = bool(re.search(r"[A-Z]", password))
        has_lower = bool(re.search(r"[a-z]", password))
        has_digit = bool(re.search(r"\d", password))
        has_special = bool(re.search(r"[!@#$%^&*()_+\-=\[\]{}|']", password))

        if sum([has_upper, has_lower, has_digit, has_special]) < 3:
            raise AppError(
                "A 'senha' deve conter pelo menos três dos seguintes tipos: "
                "letras maiúsculas, letras minúsculas, números e caracteres especiais."
            )