# execution/executors/code_executor.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class Executor(ABC):
    @abstractmethod
    def execute(self, source_code: str, input_data: str, time_limit: int, memory_limit: int) -> Dict[str, Any]:
        """Executa código com os parâmetros fornecidos"""
        pass
    
    @abstractmethod
    def get_language(self) -> str:
        """Retorna a linguagem suportada por este executor"""
        pass