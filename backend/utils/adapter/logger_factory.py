# utils/logger_factory.py
import os
from utils.interfaces.logger import LoggerInterface
from utils.adapter.console_logger_adapter import ConsoleLoggerAdapter
from utils.adapter.json_logger_adapter import JsonLoggerAdapter

class LoggerType:
    CONSOLE = "console"
    JSON = "json"
    DATABASE = "database"  # Para futuro

class LoggerFactory:
    """Fábrica para criar diferentes adaptadores de log"""
    
    @staticmethod
    def create_logger(logger_type: str = None, **kwargs) -> LoggerInterface:
        """
        Cria um logger do tipo especificado
        
        Args:
            logger_type: 'console', 'json', ou 'database'
            **kwargs: Argumentos adicionais para o logger
        
        Returns:
            LoggerInterface: Instância do logger configurado
        """
        # Se não especificado, usar variável de ambiente
        if logger_type is None:
            logger_type = os.getenv("LOG_ADAPTER", "console")
        
        if logger_type == LoggerType.CONSOLE:
            return ConsoleLoggerAdapter(
                use_colors=kwargs.get("use_colors", True),
                show_context=kwargs.get("show_context", True)
            )
        
        elif logger_type == LoggerType.JSON:
            return JsonLoggerAdapter(
                log_dir=kwargs.get("log_dir", "logs"),
                filename=kwargs.get("filename", "app_logs.json")
            )
        
        else:
            # Fallback para console
            return ConsoleLoggerAdapter()