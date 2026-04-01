from utils.app_error import AppError
from utils.validator import Validator

class LoginValidator(Validator):
    @staticmethod
    def validate(data: dict):
        login = data.get("login")
        password = data.get("password")

        if not login:
            raise AppError("Login é obrigatório.")

        if not password:
            raise AppError("Senha é obrigatória.")