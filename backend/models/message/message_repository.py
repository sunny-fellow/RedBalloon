from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Dict, Any

class MessageRepository(ABC):
    """
    Interface abstrata para o repositório de mensagens/comentários
    """
    @abstractmethod
    def create_message(self, session, user_id: int, content: str) -> Any:
        """
        Cria uma nova mensagem
        """
        pass
    
    @abstractmethod
    def create_message_context(self, session, message_id: int, context_type: str,
                               context_ref_id: Optional[int] = None,
                               parent_message: Optional[int] = None) -> None:
        """
        Cria o contexto de uma mensagem
        """
        pass
    
    @abstractmethod
    def associate_tags(self, session, message_id: int, tags: List[str]) -> None:
        """
        Associa tags a uma mensagem
        """
        pass
    
    @abstractmethod
    def get_comments(self, session, context_type: str, 
                    context_ref_id: Optional[int] = None,
                    query: Optional[str] = None, 
                    tags: Optional[List[str]] = None,
                    offset: int = 0, limit: int = 50) -> Tuple[List[Any], Dict[int, Dict[str, int]]]:
        """
        Retorna comentários de um contexto com contagem de reações
        """
        pass