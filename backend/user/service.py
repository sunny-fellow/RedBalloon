from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone

from database.service import DatabaseService
from utils.singleton import Singleton
from utils.app_error import AppError

from models.user.user import User
from user.repository import UserRepository
from user.validators.nickname_validator import NicknameValidator
from user.validators.password_validator import PasswordValidator


@Singleton
class UserService:

    def __init__(self):
        self.db_service = DatabaseService()
        self.repository = UserRepository()
        self.nickname_validator = NicknameValidator()
        self.password_validator = PasswordValidator()

    # --- CRUD ---

    def list_users(self):

        def func(session):
            users = self.repository.get_all(session)
            return [self._to_dict(u) for u in users]

        return self.db_service.run(func)

    def get_user(self, user_id: int):

        def func(session):
            user = self.repository.get_by_id(session, user_id)
            return self._to_dict(user) if user else None

        return self.db_service.run(func)

    def update_user(self, user_id: int, data: dict):

        def func(session):

            user = self.repository.get_by_id(session, user_id)

            if not user:
                return None

            if "nickname" in data:
                self.nickname_validator.validate(data["nickname"])
                user.nickname = data["nickname"]

            if "password" in data:
                self.password_validator.validate(data["password"])
                user.password = data["password"]

            for field in ["name", "email", "avatar", "description", "nationality"]:
                if field in data:
                    setattr(user, field, data[field])

            try:
                session.flush()
            except IntegrityError as e:
                raise AppError("Nickname ou email já estão em uso.") from e

            return self._to_dict(user)

        return self.db_service.run(func, user_id)

    def delete_user(self, user_id: int):

        def func(session):

            user = self.repository.get_by_id(session, user_id)

            if not user:
                return False

            self.repository.delete(session, user)

            return True

        return self.db_service.run(func, user_id)

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