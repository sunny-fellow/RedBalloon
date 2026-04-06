# message/service.py (modificado com logger)
from models.factories.sqlalchemy_factory import SQLAlchemyRepositoryFactory
from utils.app_error import AppError
from utils.singleton import Singleton
from utils.adapter.json_logger_adapter import JsonLoggerAdapter

from database.service import DatabaseService
from models.enums import MessageContextType

from message.validators.comment import CommentValidator
from message.validators.get_comments import GetCommentsValidator

from utils.adapter.logger_factory import LoggerFactory  # Adicionar import

@Singleton
class MessageService:
    def __init__(self, logger_type: str = None):
        self.db_service = DatabaseService()
        factory = SQLAlchemyRepositoryFactory()
        self.repository = factory.create_message_repository()
        
        # Criar logger usando a fábrica
        self.logger = LoggerFactory.create_logger(logger_type)

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

            # Log da criação do comentário
            log_context = {
                "message_id": message.message_id,
                "user_id": user_id,
                "context_type": context_type,
                "action": "create_comment"
            }
            
            if context_ref_id:
                log_context["context_ref_id"] = context_ref_id
            
            if parent_message:
                log_context["parent_message"] = parent_message
            
            if tags:
                log_context["tags"] = tags
            
            self.logger.info(
                f"Comentário criado no contexto {context_type}",
                context=log_context
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
            self.logger.warning(
                f"Tentativa de consulta com context_type inválido",
                context={
                    "context_type": context_type,
                    "user_id": current_user_id,
                    "action": "get_comments"
                }
            )
            raise AppError("context_type inválido", 400)
        
        if context_type in ["PROBLEM", "SOLUTION"] and not context_ref_id:
            self.logger.warning(
                f"Tentativa de consulta sem context_ref_id obrigatório",
                context={
                    "context_type": context_type,
                    "user_id": current_user_id,
                    "action": "get_comments"
                }
            )
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
                
                # Verificar se o usuário atual reagiu
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
                    "user_reaction": user_reaction
                })

            # Log da consulta
            log_context = {
                "context_type": context_type,
                "user_id": current_user_id,
                "result_count": len(result),
                "action": "get_comments"
            }
            
            if context_ref_id:
                log_context["context_ref_id"] = context_ref_id
            
            if query:
                log_context["query"] = query
            
            if tags:
                log_context["tags"] = tags
            
            if offset:
                log_context["offset"] = offset
            
            log_level = "debug" if len(result) == 0 else "info"
            
            if log_level == "debug":
                self.logger.debug(
                    f"Consulta de comentários retornou vazia",
                    context=log_context
                )
            else:
                self.logger.info(
                    f"Consulta de comentários realizada",
                    context=log_context
                )

            return result

        return self.db_service.run(func)