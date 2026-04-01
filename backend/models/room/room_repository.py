from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Any, Dict

class RoomRepository(ABC):
    """Interface abstrata para o repositório de salas"""
    
    @abstractmethod
    def list(self, session, query: Optional[str] = None) -> List[Any]:
        """
        Lista salas disponíveis com seus participantes e criador
        
        Returns:
            Lista de tuplas com: room_id, name, description, max_participants,
            ends_at, current_players, creator_name
        """
        pass
    
    @abstractmethod
    def create_room(self, session, data: Dict[str, Any]) -> Tuple[Any, str]:
        """
        Cria uma nova sala
        
        Args:
            data: Dicionário com room_name, room_description, room_password,
                  capacity, ends_at
        
        Returns:
            Tupla (sala_criada, socket_da_sala)
        """
        pass
    
    @abstractmethod
    def add_participant(self, session, room_id: int, user_id: int, is_admin: bool = False) -> Tuple[Any, str]:
        """
        Adiciona um participante à sala
        
        Returns:
            Tupla (participante, socket_do_participante)
        """
        pass
    
    @abstractmethod
    def create_problem(self, session, data: Dict[str, Any]) -> Any:
        """
        Cria um novo problema
        
        Returns:
            Problema criado
        """
        pass
    
    @abstractmethod
    def add_problem_to_room(self, session, room_id: int, problem_id: int, points: int, balloon: str) -> None:
        """
        Adiciona um problema à sala com pontuação e balão
        """
        pass
    
    @abstractmethod
    def get_room_by_id(self, session, room_id: int) -> Optional[Any]:
        """
        Busca uma sala pelo ID
        """
        pass
    
    @abstractmethod
    def count_participants(self, session, room_id: int) -> int:
        """
        Conta o número de participantes em uma sala
        """
        pass