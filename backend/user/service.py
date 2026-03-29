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

    def list_users(self, data):

        def func(session):
            users = self.repository.get_all(
                session,
                query=data.get("query", ""),
                country=data.get("country", "")
            )

            return [
                {
                    "user_id": u.user_id,
                    "name": u.name,
                    "avatar": u.avatar,
                    "followers": u.followers_count,
                    "solved": u.solved_count,
                    "nationality": u.nationality
                }
                for u in users
            ]

        return self.db_service.run(func)

    def get_user(self, data):
        user_id = data.get("user_id")
        requester_id = data.get("requester_id")

        def func(session):
            result = self.repository.get_user_full(session, user_id, requester_id)

            if not result:
                return None

            user, solved, created = result

            return {
                "user_id": user.user_id,
                "name": user.name,
                "avatar": user.avatar,
                "nationality": user.nationality,
                "followers": user.followers_count,
                "description": user.description,
                "solved": user.solved_count,
                "is_following": user.is_following > 0,

                "solved_problems": [
                    {
                        "problem_id": p.problem_id,
                        "title": p.title,
                        "difficulty": p.difficulty
                    }
                    for p in solved
                ],

                "created_problems": [
                    {
                        "problem_id": p.problem_id,
                        "title": p.title,
                        "difficulty": p.difficulty,
                        "solved_count": p.solved_count
                    }
                    for p in created
                ]
            }

        return self.db_service.run(func)
    
    def follow(self, data):
        follower_id = data.get("follower_id")
        following_id = data.get("following_id")

        def func(session):
            if follower_id == following_id:
                raise AppError("Você não pode seguir a si mesmo", 401)

            existing = self.repository.get_follow(
                session, follower_id, following_id
            )

            if existing:
                self.repository.delete_follow(session, existing)
                return {"following": False}

            self.repository.create_follow(
                session, follower_id, following_id
            )
            return {"following": True}

        return self.db_service.run(func)

    def update_user(self, user_id: int, data: dict):

        def func(session):

            if not self.repository.user_exists(session, user_id):
                return False

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

            if not self.repository.user_exists(session, user_id):
                return False

            self.repository.delete(session, user_id)

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
    
    def count_users(self):
        def func(session):
            return self.repository.count_users(session)

        return self.db_service.run(func)