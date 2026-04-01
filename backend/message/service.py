from models.factories.sqlalchemy_factory import SQLAlchemyRepositoryFactory
from utils.app_error import AppError
from utils.singleton import Singleton

from database.service import DatabaseService
from models.enums import MessageContextType

from message.validators.comment import CommentValidator
from message.validators.get_comments import GetCommentsValidator


@Singleton
class MessageService:
    def __init__(self):
        self.db_service = DatabaseService()
        factory = SQLAlchemyRepositoryFactory()
        self.repository = factory.create_message_repository()

    def comment(self, data):
        CommentValidator.validate(data)

        user_id = data["user_id"]
        message_text = data["message"].strip()
        context_type = data["context_type"]
        context_ref_id = data.get("context_ref_id")
        parent_message = data.get("parent_message")
        tags = data.get("tags")

        def func(session):
            message = self.repository.create_message(session, user_id, message_text)

            self.repository.create_message_context(
                session,
                message_id=message.message_id,
                context_type=context_type,
                context_ref_id=context_ref_id,
                parent_message=parent_message
            )

            self.repository.associate_tags(
                session,
                message_id=message.message_id,
                tags=tags
            )

            return {
                "message_id": message.message_id,
                "message": message.message,
                "sent_at": message.sent_at
            }

        return self.db_service.run(func, user_id=user_id)
    
    def get_comments(self, data):
        """
        Retorna comentários filtrados por contexto, query, tags
        e inclui likes/dislikes da mensagem.
        """
        GetCommentsValidator.validate(data)

        context_type = data.get("context_type")
        context_ref_id = data.get("context_ref_id")
        query = data.get("query")
        tags = data.get("tags")
        current_user_id = data.get("user_id")
        offset = data.get("offset")

        if context_type not in ["GLOBAL", "PROBLEM", "SOLUTION"]:
            raise AppError("context_type inválido", 400)
        
        if context_type in ["PROBLEM", "SOLUTION"] and not context_ref_id:
            raise AppError("context_ref_id é obrigatório para este context_type", 400)

        def func(session):
            comments, reacts = self.repository.get_comments(
                session=session,
                context_type=context_type,
                context_ref_id=context_ref_id,
                query=query,
                tags=tags
            )
            result = []
            
            for msg in comments:
                msg_tags = [t.tag for t in getattr(msg, "tags", [])]
                reaction_info = reacts.get(msg.message_id, {"likes": 0, "dislikes": 0})
                
                # Opcional: verificar se o usuário atual reagiu
                user_reaction = None
                
                if current_user_id:
                    react = next(
                        (r for r in getattr(msg, "likes", []) if r.user_id == current_user_id),
                        None
                    )
                    user_reaction = react.reaction.value if react else None

                result.append({
                    "message_id": msg.message_id,
                    "user_id": msg.user_id,
                    "user_name": msg.user.name if msg.user else None,
                    "message": msg.message,
                    "sent_at": msg.sent_at,
                    "tags": msg_tags,
                    "parent_message": getattr(msg.context, "parent_message", None),
                    "likes": reaction_info["likes"],
                    "dislikes": reaction_info["dislikes"],
                    "user_reaction": user_reaction  # "LIKE" | "DISLIKE" | None
                })

            return result

        return self.db_service.run(func)