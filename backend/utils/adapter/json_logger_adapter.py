import json
import os
from datetime import datetime
from threading import Lock
from utils.interfaces.logger import LoggerInterface

class JsonLoggerAdapter(LoggerInterface):
    """Adapter para armazenar logs em arquivo JSON"""
    
    def __init__(self, log_dir: str = "logs", filename: str = "user_actions.json"):
        self.log_dir = log_dir
        self.filename = filename
        self.filepath = os.path.join(log_dir, filename)
        self._lock = Lock()  # Para evitar conflitos em requisições concorrentes
        
        # Cria diretório se não existir
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Inicializa arquivo se não existir
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump([], f)
    
    def info(self, message: str, context: dict = None) -> None:
        self._save_log("INFO", message, context)
    
    def error(self, message: str, context: dict = None) -> None:
        self._save_log("ERROR", message, context)
    
    def warning(self, message: str, context: dict = None) -> None:
        self._save_log("WARNING", message, context)
    
    def debug(self, message: str, context: dict = None) -> None:
        self._save_log("DEBUG", message, context)
    
    def _save_log(self, level: str, message: str, context: dict = None) -> None:
        """Salva o log no arquivo JSON"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "context": context or {}
        }
        
        # Usa lock para evitar corrupção do arquivo em requisições concorrentes
        with self._lock:
            try:
                # Lê logs existentes
                with open(self.filepath, 'r') as f:
                    logs = json.load(f)
                
                # Adiciona novo log
                logs.append(log_entry)
                
                # Escreve de volta
                with open(self.filepath, 'w') as f:
                    json.dump(logs, f, indent=2, ensure_ascii=False)
                    
            except Exception as e:
                # Fallback: se falhar, escreve em arquivo separado
                self._save_fallback(level, message, context, str(e))
    
    def _save_fallback(self, level: str, message: str, context: dict, error: str):
        """Fallback em caso de erro no JSON"""
        fallback_file = os.path.join(self.log_dir, "logs_fallback.txt")
        with open(fallback_file, 'a') as f:
            f.write(f"[{level}] {message} | Context: {context} | Error: {error}\n")
    
    def get_logs(self, level: str = None, limit: int = 100):
        """Método utilitário para consultar logs"""
        try:
            with open(self.filepath, 'r') as f:
                logs = json.load(f)
            
            if level:
                logs = [log for log in logs if log['level'] == level.upper()]
            
            return logs[-limit:]  # Retorna os mais recentes
        except Exception:
            return []
    
    def clear_logs(self):
        """Limpa todos os logs (útil para testes)"""
        with self._lock:
            with open(self.filepath, 'w') as f:
                json.dump([], f)