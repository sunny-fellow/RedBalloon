from models.message.message_repository import MessageRepository
from sqlalchemy import or_, func

from models.message.message import Message
from models.message.message_context import MessageContext
from models.message.message_tag import MessageTag
from models.message.message_react import MessageReact
from models.user.user import User
from models.enums import MessageContextType, ReactionType

class SQLAlchemyMessageRepository(MessageRepository):
    def create_message(self, session, user_id: int, content: str) -> Message:
        """
        Cria a mensagem e retorna o objeto.
        """
        message = Message(user_id=user_id, message=content)
        session.add(message)
        session.flush()  # Gera o message_id
        return message

    def create_message_context(self, session, message_id: int, context_type: str,
                               context_ref_id: int = None, parent_message: int = None):
        """
        Cria o contexto da mensagem.
        """
        context = MessageContext(
            message_id=message_id,
            context_type=MessageContextType(context_type),
            context_ref_id=context_ref_id,
            parent_message=parent_message
        )
        session.add(context)

    def associate_tags(self, session, message_id, tags):
        for tag in tags:
            session.add(MessageTag(message_id=message_id, tag=tag))

    def get_comments(self, session, context_type: str,
                     context_ref_id: int = None, query: str = None, tags: list[str] = None,
                     offset: int = 0, limit: int = 50):
        """
        Retorna lista de mensagens de um determinado contexto, com contagem de likes/dislikes.
        Ordena por: mais likes primeiro, depois mais recente. Aplica offset e limite.
        """
        # Base query
        base_query = session.query(Message).join(MessageContext)

        # Filtro por contexto
        base_query = base_query.filter(MessageContext.context_type == context_type)
        
        if context_type in ["PROBLEM", "SOLUTION"]:
            base_query = base_query.filter(MessageContext.context_ref_id == context_ref_id)

        # Filtro textual
        base_query = self._apply_text_filter(base_query, query)

        # Filtro por tags
        base_query = self._apply_tag_filter(base_query, tags)

        # Ordenar no SQL
        base_query = base_query.outerjoin(MessageReact).group_by(Message.message_id).order_by(
                                func.coalesce(func.sum(func.case([(MessageReact.reaction == ReactionType.LIKE, 1)], else_=0)), 0).desc(),
                                Message.sent_at.desc()
                            )

        # Aplicar offset e limite
        comments = base_query.offset(offset).limit(limit).all()
        message_ids = [msg.message_id for msg in comments]

        # Contagem de likes/dislikes
        reacts = self._get_reacts(session, message_ids)

        return comments, reacts

    # Filtros auxiliares
    def _apply_text_filter(self, query_obj, search_text):
        if search_text:
            search = f"%{search_text}%"
            query_obj = query_obj.join(User).filter(
                or_(
                    Message.message.ilike(search),
                    User.name.ilike(search),
                    User.nickname.ilike(search)
                )
            )
        return query_obj

    def _apply_tag_filter(self, query_obj, tags):
        if tags:
            query_obj = query_obj.join(MessageTag).filter(MessageTag.tag.in_(tags))
        
        return query_obj

    # Contagem de reações
    def _get_reacts(self, session, message_ids):
        reacts = {}
        
        if not message_ids:
            return reacts

        rows = session.query(
            MessageReact.message_id,
            MessageReact.reaction,
            func.count().label("count")
        ).filter(MessageReact.message_id.in_(message_ids)) \
         .group_by(MessageReact.message_id, MessageReact.reaction) \
         .all()

        for row in rows:
            if row.message_id not in reacts:
                reacts[row.message_id] = {"likes": 0, "dislikes": 0}
            
            if row.reaction == ReactionType.LIKE:
                reacts[row.message_id]["likes"] = row.count
            
            else:
                reacts[row.message_id]["dislikes"] = row.count

        return reacts