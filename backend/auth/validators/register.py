import re
from utils.validation_error import ValidationError
from user.validators.nickname_validator import NicknameValidator
from user.validators.password_validator import PasswordValidator

class RegisterValidator:

    @staticmethod
    def validate(data: dict):

        required_fields = [
            "name",
            "nickname",
            "email",
            "password",
            "nationality"
        ]

        for field in required_fields:
            if not data.get(field):
                raise ValidationError(f"{field} é obrigatório.")

        email = data["email"]

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Email inválido.")

        password = data["password"]
        nickname = data["nickname"]

        PasswordValidator().validate(password)
        NicknameValidator().validate(nickname)