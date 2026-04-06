# listeners/notification_listener.py
from event_bus import EventListener, Event, EventType
from utils.adapter.json_logger_adapter import JsonLoggerAdapter
from datetime import datetime

class NotificationListener(EventListener):
    """Registra notificações para usuários sobre eventos relevantes"""
    
    def __init__(self):
        self.logger = JsonLoggerAdapter("logs", "notifications.json")
    
    def handle(self, event: Event):
        if event.type == EventType.SUBMISSION_ACCEPTED:
            user_id = event.payload["user_id"]
            problem_id = event.payload["problem_id"]
            submission_id = event.payload.get("submission_id")
            
            # Registra a notificação no log
            self.logger.info(
                f"Submissão aceita - notificação gerada",
                context={
                    "type": "submission_accepted",
                    "user_id": user_id,
                    "problem_id": problem_id,
                    "submission_id": submission_id,
                    "timestamp": datetime.now().isoformat(),
                    "message": f"Parabéns! Você resolveu o problema {problem_id}!"
                }
            )
            
            # Aqui você pode expandir depois para:
            # - Salvar notificação no banco de dados
            # - Enviar email
            # - Enviar push notification
            # - Atualizar feed do usuário
        
        elif event.type == EventType.USER_FOLLOWED:
            follower_id = event.payload["follower_id"]
            following_id = event.payload["following_id"]
            
            self.logger.info(
                f"Novo seguidor - notificação gerada",
                context={
                    "type": "new_follower",
                    "follower_id": follower_id,
                    "following_id": following_id,
                    "timestamp": datetime.now().isoformat(),
                    "message": f"Usuário {follower_id} começou a seguir você!"
                }
            )