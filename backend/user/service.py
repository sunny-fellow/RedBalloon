import re
from sqlalchemy.exc import IntegrityError
from database.service import DatabaseService
from models.user.user import User
from datetime import datetime, timezone
from utils.singleton import Singleton

class ValidationError(Exception):
    pass

@Singleton
class UserService:
    def __init__(self):
        self.db_service = DatabaseService()

    # --- validações ---
    def _validate_nickname(self, nickname: str):
        if not nickname or not nickname.strip():
            raise ValidationError("O campo 'nickname' não pode ser vazio.")
        if len(nickname) > 12:
            raise ValidationError("O 'nickname' deve ter no máximo 12 caracteres.")
        if re.search(r'\d', nickname):
            raise ValidationError("O 'nickname' não pode conter números.")

    def _validate_password(self, password: str):
        if not password:
            raise ValidationError("O campo 'password' não pode ser vazio.")
        if len(password) < 8 or len(password) > 128:
            raise ValidationError("A 'senha' deve ter entre 8 e 128 caracteres.")

        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r"[!@#$%^&*()_+\-=\[\]{}|']", password))

        if sum([has_upper, has_lower, has_digit, has_special]) < 3:
            raise ValidationError(
                "A 'senha' deve conter pelo menos três dos seguintes tipos: "
                "letras maiúsculas, letras minúsculas, números e caracteres especiais."
            )

    # --- CRUD ---
    def list_users(self):
        def func(session):
            users = session.query(User).all()
            return [self._to_dict(u) for u in users]
        return self.db_service.run(func)

    def create_user(self, data: dict):
        nickname = data.get("nickname")
        password = data.get("password")
        email = data.get("email")

        self._validate_nickname(nickname)
        self._validate_password(password)
        if not email:
            raise ValidationError("O campo 'email' é obrigatório.")

        new_user = User(
            nickname=nickname,
            password=password,  # trocar para hash futuramente
            email=email,
            name=data.get("name"),
            avatar=data.get("avatar"),
            description=data.get("description"),
            nationality=data.get("nationality"),
            created_at=datetime.now(timezone.utc).isoformat()
        )

        def func(session):
            session.add(new_user)
            try:
                session.flush()  # força validação de constraints antes do commit
            except IntegrityError as e:
                raise ValidationError("Nickname ou email já estão em uso.") from e
            return self._to_dict(new_user)

        return self.db_service.run(func)

    def get_user(self, user_id: int):
        def func(session):
            user = session.query(User).filter(User.user_id == user_id).first()
            return self._to_dict(user) if user else None
        return self.db_service.run(func)

    def update_user(self, user_id: int, data: dict):
        def func(session):
            user: User = session.query(User).filter(User.user_id == user_id).first()
            if not user:
                return None

            if "nickname" in data:
                self._validate_nickname(data["nickname"])
                user.nickname = data["nickname"]

            if "password" in data:
                self._validate_password(data["password"])
                user.password = data["password"]

            for field in ["name", "email", "avatar", "description", "nationality"]:
                if field in data:
                    setattr(user, field, data[field])

            try:
                session.flush()
            except IntegrityError as e:
                raise ValidationError("Nickname ou email já estão em uso.") from e

            return self._to_dict(user)

        return self.db_service.run(func)

    def delete_user(self, user_id: int):
        def func(session):
            user: User = session.query(User).filter(User.user_id == user_id).first()
            if not user:
                return False
            session.delete(user)
            return True

        return self.db_service.run(func)

    # --- utilitário ---
    def _to_dict(self, user: User):
        return {
            "user_id": user.user_id,
            "nickname": user.nickname,
            "name": user.name,
            "email": user.email,
            "avatar": user.avatar,
            "description": user.description,
            "nationality": user.nationality,
            "created_at": user.created_at
        }