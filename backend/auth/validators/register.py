import re
from utils.app_error import AppError
from utils.interfaces.validator import Validator
from user.validators.nickname_validator import NicknameValidator
from user.validators.password_validator import PasswordValidator

class RegisterValidator(Validator):
    @staticmethod
    def validate(data: dict):
        required_fields = ["name", "nickname", "email", "password", "nationality"]

        for field in required_fields:
            if not data.get(field):
                raise AppError(f"{field} é obrigatório.")

        email = data["email"]

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise AppError("Email inválido.")

        password = data["password"]
        nickname = data["nickname"]

        print("Password", password)

        PasswordValidator.validate(password)
        NicknameValidator.validate(nickname)