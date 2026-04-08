from datetime import datetime
import json
from utils.interfaces.logger import LoggerInterface

class ConsoleLoggerAdapter(LoggerInterface):
    """
    Adapter para logging no console com cores (opcional)
    """
    class Colors:
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
    
    def __init__(self, use_colors: bool = True, show_context: bool = True):
        self.use_colors = use_colors
        self.show_context = show_context
    
    def info(self, message: str, context: dict = None) -> None:
        self._log("INFO", message, context, self.Colors.GREEN if self.use_colors else "")
    
    def error(self, message: str, context: dict = None) -> None:
        self._log("ERROR", message, context, self.Colors.RED if self.use_colors else "")
    
    def warning(self, message: str, context: dict = None) -> None:
        self._log("WARNING", message, context, self.Colors.YELLOW if self.use_colors else "")
    
    def debug(self, message: str, context: dict = None) -> None:
        self._log("DEBUG", message, context, self.Colors.CYAN if self.use_colors else "")
    
    def _log(self, level: str, message: str, context: dict = None, color: str = "") -> None:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Formatar a mensagem
        log_message = f"{timestamp} [{level}] {message}"
        
        # Adicionar contexto se necessário
        if self.show_context and context:
            context_str = json.dumps(context, ensure_ascii=False, default=str)
            log_message += f"\n       Context: {context_str}"
        
        # Aplicar cor se disponível
        if color and self.use_colors:
            log_message = f"{color}{log_message}{self.Colors.RESET}"
        
        # Imprimir no console
        print(log_message)