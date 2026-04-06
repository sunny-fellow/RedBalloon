# execution/execution_context.py
from typing import Dict, Any, Optional
from execution.executors.code_executor import Executor
from execution.executors import PythonExecutor, CExecutor, CppExecutor, JavaExecutor

class ExecutionContext:
    """Contexto que gerencia a estratégia de execução"""
    
    def __init__(self):
        self._strategies: Dict[str, Executor] = {}
        self._current_strategy: Optional[Executor] = None
        self._register_default_strategies()
    
    def _register_default_strategies(self):
        """Registra todas as estratégias disponíveis"""
        strategies = [
            PythonExecutor(),
            CExecutor(),
            CppExecutor(),
            JavaExecutor()
        ]
        
        for strategy in strategies:
            self.register_strategy(strategy.get_language(), strategy)
    
    def register_strategy(self, language: str, executor: Executor):
        """Registra uma nova estratégia para uma linguagem"""
        self._strategies[language.upper()] = executor
    
    def set_strategy(self, language: str):
        """Define a estratégia a ser usada baseada na linguagem"""
        language_upper = language.upper()
        
        if language_upper not in self._strategies:
            raise ValueError(f"Unsupported language: {language}")
        
        self._current_strategy = self._strategies[language_upper]
    
    def execute(self, source_code: str, input_data: str, 
                time_limit: int, memory_limit: int) -> Dict[str, Any]:
        """Executa o código usando a estratégia atual"""
        if not self._current_strategy:
            raise ValueError("No strategy selected. Call set_strategy() first.")
        
        return self._current_strategy.execute(
            source_code, input_data, time_limit, memory_limit
        )
    
    def get_supported_languages(self) -> list:
        """Retorna lista de linguagens suportadas"""
        return list(self._strategies.keys())
    
    def has_strategy(self, language: str) -> bool:
        """Verifica se existe estratégia para determinada linguagem"""
        return language.upper() in self._strategies