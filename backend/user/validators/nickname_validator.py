import re
from utils.validation_error import ValidationError

class NicknameValidator:

    def validate(self, nickname: str):

        if not nickname or not nickname.strip():
            raise ValidationError("O campo 'nickname' não pode ser vazio.")

        if len(nickname) > 12:
            raise ValidationError("O 'nickname' deve ter no máximo 12 caracteres.")

        if re.search(r"\d", nickname):
            raise ValidationError("O 'nickname' não pode conter números.")