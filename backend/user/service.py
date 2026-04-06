# user/service.py (completo)
from models.factories.sqlalchemy_factory import SQLAlchemyRepositoryFactory
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone

from database.service import DatabaseService
from utils.singleton import Singleton
from utils.app_error import AppError
from utils.adapter.json_logger_adapter import JsonLoggerAdapter

from models.user.user import User
from models.factories.repository_factory import RepositoryFactory
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
        
        # Adapter para JSON logs
        self.logger = JsonLoggerAdapter(log_dir="logs", filename="user_actions.json")

    def list_users(self, data):
        def func(session):
            users = self.repository.get_all(
                session,
                query=data.get("query", ""),
                country=data.get("country", "")
            )
            
            self.logger.debug(
                f"Listagem de usuários realizada",
                context={
                    "query": data.get("query", ""),
                    "country": data.get("country", ""),
                    "result_count": len(users),
                    "action": "list"
                }
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
                self.logger.warning(
                    f"Tentativa de acesso a usuário inexistente",
                    context={
                        "user_id": user_id,
                        "requester_id": requester_id,
                        "action": "get_user"
                    }
                )
                return None

            user, solved, created = result
            
            self.logger.info(
                f"Perfil de usuário acessado",
                context={
                    "user_id": user_id,
                    "requester_id": requester_id,
                    "action": "view_profile"
                }
            )
            
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
                self.logger.warning(
                    "Tentativa de auto-follow",
                    context={
                        "user_id": follower_id,
                        "action": "follow"
                    }
                )
                raise AppError("Você não pode seguir a si mesmo", 401)

            # Verificar se o usuário a ser seguido existe e está ativo
            user_to_follow = self.repository.get_by_id(session, following_id)
            if not user_to_follow:
                self.logger.warning(
                    "Tentativa de seguir usuário inexistente",
                    context={
                        "follower_id": follower_id,
                        "target_id": following_id,
                        "action": "follow"
                    }
                )
                raise AppError("Usuário não encontrado ou está inativo", 404)

            existing = self.repository.get_follow(
                session, follower_id, following_id
            )
            if existing:
                self.repository.delete_follow(session, existing)
                self.logger.info(
                    "Unfollow realizado",
                    context={
                        "follower_id": follower_id,
                        "following_id": following_id,
                        "action": "unfollow"
                    }
                )
                return {"following": False}

            self.repository.create_follow(
                session, follower_id, following_id
            )
            self.logger.info(
                "Follow realizado",
                context={
                    "follower_id": follower_id,
                    "following_id": following_id,
                    "action": "follow"
                }
            )
            return {"following": True}

        return self.db_service.run(func)

    def update_user(self, user_id: int, data: dict):
        def func(session):
            if not self.repository.user_exists(session, user_id):
                self.logger.error(
                    f"Tentativa de atualizar usuário inexistente",
                    context={
                        "user_id": user_id,
                        "action": "update"
                    }
                )
                return False

            user = self.repository.get_by_id(session, user_id)

            if not user:
                return None

            # Registra alterações para log
            changes = {}
            
            if "nickname" in data and data["nickname"] != user.nickname:
                changes["nickname"] = {"old": user.nickname, "new": data["nickname"]}
                self.nickname_validator.validate(data["nickname"])
                user.nickname = data["nickname"]

            if "password" in data:
                changes["password"] = {"changed": True}
                self.password_validator.validate(data["password"])
                user.password = data["password"]

            for field in ["name", "email", "avatar", "description", "nationality"]:
                if field in data and getattr(user, field) != data[field]:
                    changes[field] = {"old": getattr(user, field), "new": data[field]}
                    setattr(user, field, data[field])

            try:
                session.flush()
                
                if changes:
                    self.logger.info(
                        f"Usuário atualizado",
                        context={
                            "user_id": user_id,
                            "action": "update",
                            "changes": changes
                        }
                    )
            
            except IntegrityError as e:
                self.logger.error(
                    f"Erro de integridade ao atualizar usuário",
                    context={
                        "user_id": user_id,
                        "error": str(e),
                        "action": "update"
                    }
                )
                raise AppError("Nickname ou email já estão em uso.") from e

            return self._to_dict(user)

        return self.db_service.run(func, user_id)

    def delete_user(self, user_id: int):
        def func(session):
            if not self.repository.user_exists(session, user_id):
                self.logger.warning(
                    f"Tentativa de deletar usuário inexistente",
                    context={
                        "user_id": user_id,
                        "action": "delete"
                    }
                )
                return False

            # Aplica soft delete
            result = self.repository.soft_delete(session, user_id)
            
            if result:
                self.logger.info(
                    f"Usuário deletado (soft delete)",
                    context={
                        "user_id": user_id,
                        "action": "soft_delete"
                    }
                )

            return result

        return self.db_service.run(func, user_id)

    def restore_user(self, user_id: int):
        """Método para restaurar usuário deletado"""
        def func(session):
            result = self.repository.restore(session, user_id)
            
            if result:
                self.logger.info(
                    f"Usuário restaurado",
                    context={
                        "user_id": user_id,
                        "action": "restore"
                    }
                )
            else:
                self.logger.warning(
                    f"Tentativa de restaurar usuário inexistente ou não deletado",
                    context={
                        "user_id": user_id,
                        "action": "restore"
                    }
                )
            
            return result

        return self.db_service.run(func, user_id)

    def permanent_delete_user(self, user_id: int):
        """Método para exclusão física (apenas se realmente necessário)"""
        def func(session):
            # Primeiro verificar se não há dados importantes
            user = self.repository.get_by_id_including_deleted(session, user_id)
            if not user:
                self.logger.warning(
                    f"Tentativa de exclusão permanente de usuário inexistente",
                    context={
                        "user_id": user_id,
                        "action": "permanent_delete"
                    }
                )
                return False
            
            result = self.repository.permanent_delete(session, user_id)
            
            if result:
                self.logger.error(
                    f"Usuário permanentemente excluído",
                    context={
                        "user_id": user_id,
                        "action": "permanent_delete"
                    }
                )
            
            return result

        return self.db_service.run(func, user_id)

    def count_users(self):
        def func(session):
            count = self.repository.count_users(session)
            
            self.logger.debug(
                f"Contagem de usuários realizada",
                context={
                    "total_users": count,
                    "action": "count"
                }
            )
            
            return count

        return self.db_service.run(func)

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