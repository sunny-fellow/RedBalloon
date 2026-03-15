from utils.validation_error import ValidationError

class LoginValidator:

    @staticmethod
    def validate(data: dict):

        login = data.get("login")
        password = data.get("password")

        if not login:
            raise ValidationError("Login é obrigatório.")

        if not password:
            raise ValidationError("Senha é obrigatória.")