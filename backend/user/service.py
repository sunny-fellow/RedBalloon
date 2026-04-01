from models.factories.sqlalchemy_factory import SQLAlchemyRepositoryFactory
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone

from database.service import DatabaseService
from utils.singleton import Singleton
from utils.app_error import AppError

from models.user.user import User
from models.factories.repository_factory import RepositoryFactory  # Importa a Factory
from user.validators.nickname_validator import NicknameValidator
from user.validators.password_validator import PasswordValidator


@Singleton
class UserService:
    def __init__(self):
        self.db_service = DatabaseService()
        factory = SQLAlchemyRepositoryFactory()
        self.repository = factory.create_user_repository()
        self.nickname_validator = NicknameValidator()
        self.password_validator = PasswordValidator()

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

            # Verificar se o usuário a ser seguido existe e está ativo
            user_to_follow = self.repository.get_by_id(session, following_id)
            if not user_to_follow:
                raise AppError("Usuário não encontrado ou está inativo", 404)

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

    # MODIFICADO: Substituir delete físico por soft delete
    def delete_user(self, user_id: int):
        def func(session):
            if not self.repository.user_exists(session, user_id):
                return False

            # Aplica soft delete
            return self.repository.soft_delete(session, user_id)

        return self.db_service.run(func, user_id)

    # NOVO: Método para restaurar usuário
    def restore_user(self, user_id: int):
        def func(session):
            return self.repository.restore(session, user_id)

        return self.db_service.run(func, user_id)

    # NOVO: Método para exclusão física (apenas se realmente necessário)
    def permanent_delete_user(self, user_id: int):
        def func(session):
            # Primeiro verificar se não há dados importantes
            user = self.repository.get_by_id_including_deleted(session, user_id)
            if not user:
                return False
            
            # Opcional: verificar se o usuário tem dados que não devem ser perdidos
            # Aqui você pode adicionar lógica de negócio
            
            return self.repository.permanent_delete(session, user_id)

        return self.db_service.run(func, user_id)

    # Utilitário
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