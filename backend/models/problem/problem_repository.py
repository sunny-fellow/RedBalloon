from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Tuple

class ProblemRepository(ABC):
    """Interface do repositório de problemas"""
    
    @abstractmethod
    def list_problems(self, session, query: Optional[str] = None, tags: Optional[List[str]] = None) -> List[Any]:
        """Lista problemas com filtros opcionais"""
        pass
    
    @abstractmethod
    def get_reactions_count(self, session, problem_ids: List[int]) -> Dict[int, Dict[str, int]]:
        """Retorna contagem de likes/dislikes para múltiplos problemas"""
        pass
    
    @abstractmethod
    def get_tags(self, session, problem_ids: List[int]) -> Dict[int, List[str]]:
        """Retorna tags para múltiplos problemas"""
        pass
    
    @abstractmethod
    def get_submission_stats_bulk(self, session, problem_ids: List[int]) -> Dict[int, Dict[str, int]]:
        """Retorna estatísticas de submissões para múltiplos problemas"""
        pass
    
    @abstractmethod
    def get_problem_by_id(self, session, problem_id: int) -> Optional[Any]:
        """Busca um problema pelo ID"""
        pass
    
    @abstractmethod
    def get_creator_name(self, session, creator_id: int) -> Optional[str]:
        """Retorna o nome do criador do problema"""
        pass
    
    @abstractmethod
    def get_reactions(self, session, problem_id: int) -> Dict[str, int]:
        """Retorna contagem de likes/dislikes para um problema específico"""
        pass
    
    @abstractmethod
    def get_submission_stats_single(self, session, problem_id: int) -> Dict[str, int]:
        """Retorna estatísticas de submissões para um problema específico"""
        pass
    
    @abstractmethod
    def get_problem_tags(self, session, problem_id: int) -> List[str]:
        """Retorna tags de um problema específico"""
        pass
    
    @abstractmethod
    def get_comments(self, session, problem_id: int) -> List[Dict[str, Any]]:
        """Retorna comentários de um problema"""
        pass
    
    @abstractmethod
    def get_user_reaction(self, session, problem_id: int, user_id: int) -> Optional[str]:
        """Retorna a reação de um usuário específico para um problema"""
        pass
    
    @abstractmethod
    def upsert_problem_react(self, session, problem_id: int, user_id: int, react_type: Any) -> str:
        """Cria, atualiza ou remove uma reação (toggle)"""
        pass
    
    @abstractmethod
    def count_problems(self, session) -> int:
        """Conta o total de problemas"""
        pass