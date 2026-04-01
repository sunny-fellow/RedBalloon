from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Any

class UserRepository(ABC):
    """Interface do repositório de usuários"""
    
    @abstractmethod
    def get_all(self, session, query=None, country=None) -> List[Any]:
        pass
    
    @abstractmethod
    def get_user_full(self, session, user_id: int, requester_id: int) -> Optional[Tuple]:
        pass
    
    @abstractmethod
    def add(self, session, user) -> None:
        pass
    
    @abstractmethod
    def soft_delete(self, session, user_id: int) -> bool:
        pass
    
    @abstractmethod
    def restore(self, session, user_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_by_id(self, session, user_id: int) -> Optional[Any]:
        pass
    
    @abstractmethod
    def user_exists(self, session, user_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_follow(self, session, follower_id: int, following_id: int) -> Optional[Any]:
        pass
    
    @abstractmethod
    def create_follow(self, session, follower_id: int, following_id: int) -> Any:
        pass
    
    @abstractmethod
    def delete_follow(self, session, follow) -> None:
        pass
    
    @abstractmethod
    def count_users(self, session) -> int:
        pass