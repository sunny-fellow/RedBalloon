from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

class SubmissionRepository(ABC):
    """Interface abstrata para o repositório de submissões"""
    
    @abstractmethod
    def save_submission(self, session, problem_id: int, user_id: int, code: str, 
                       language: str, time_spent: int, status: str, submitted_at: Any) -> Any:
        """
        Salva uma nova submissão
        
        Returns:
            Objeto Submission criado
        """
        pass
    
    @abstractmethod
    def get_any_submission(self, session, problem_id: int) -> List[Any]:
        """
        Retorna todas as submissões aceitas de um problema
        """
        pass
    
    @abstractmethod
    def get_submission(self, session, submission_id: int) -> Optional[Any]:
        """
        Busca uma submissão pelo ID
        """
        pass
    
    @abstractmethod
    def get_existing_react(self, session, submission_id: int, user_id: int) -> Optional[Any]:
        """
        Busca uma reação existente em uma submissão
        
        Returns:
            Objeto SubmissionReact ou None
        """
        pass
    
    @abstractmethod
    def add_react(self, session, submission_id: int, user_id: int, reaction: Any) -> Any:
        """
        Adiciona uma reação a uma submissão
        
        Returns:
            Objeto SubmissionReact criado
        """
        pass
    
    @abstractmethod
    def remove_react(self, session, react: Any) -> None:
        """
        Remove uma reação de uma submissão
        """
        pass
    
    @abstractmethod
    def update_react(self, react: Any, reaction: Any) -> None:
        """
        Atualiza uma reação existente
        """
        pass
    
    @abstractmethod
    def get_submission_details(self, session, submission_id: int, requesting_user_id: int) -> Optional[Dict[str, Any]]:
        """
        Retorna detalhes completos de uma submissão
        
        Returns:
            Dicionário com: submission_id, time_spent, memory_used, creator_id, 
            creator_name, creator_avatar, code, language, likes, dislikes, 
            user_reaction, problem_id, problem_title, problem_creator_name,
            problem_description, problem_difficulty, problem_tags
        """
        pass