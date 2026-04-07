# room/gateway.py
from functools import wraps
from flask_socketio import Namespace, emit
from utils.app_error import AppError
from room.gateway.service import RoomGatewayService

service = RoomGatewayService()

def safe_emit(event_name, broadcast=False):
    """
    Decorator para capturar erros do service e enviar para o cliente.
        - Se broadcast = True, envia para a sala (room_socket).  
        - Se broadcast = False, envia apenas para o usuário (user_socket).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, data):
            try:
                result = func(self, data)
                
                if broadcast:
                    # Envia para todos na sala
                    emit(event_name, {"status": "success", "data": result}, room=data.get("room_socket"))
                
                else:
                    # Envia apenas para o usuário que acionou
                    emit(event_name, {"status": "success", "data": result}, to=data.get("user_socket"))
            
            except AppError as e:
                emit(event_name, {"status": "error", "message": str(e)}, to=data.get("user_socket"))
            
            except Exception as e:
                emit(event_name, {"status": "error", "message": "Erro interno"}, to=data.get("user_socket"))
                print("ERRO:", e)
        
        return wrapper    
    
    return decorator

class RoomGateway(Namespace):
    def on_connect(self):
        print("Cliente conectado")

    def on_disconnect(self):
        print("Cliente desconectado")

    @safe_emit("new_message", broadcast=True)
    def on_send_message(self, data):
        return service.send_message(data)

    @safe_emit("submission_result")
    def on_submit_problem(self, data):
        return service.submit_problem(data)

    @safe_emit("room_config_updated")
    def on_update_room_config(self, data):
        return service.update_room_config(data)

    @safe_emit("room_problems")
    def on_get_room_problems(self, data):
        return service.get_room_problems(data["room_id"])

    @safe_emit("lobby_info")
    def on_get_lobby_info(self, data):
        return service.get_room_lobby_info(data)

    @safe_emit("problem_details")
    def on_get_problem_details(self, data):
        return service.get_problem_details(data)

    @safe_emit("user_submissions")
    def on_get_my_submissions(self, data):
        return service.get_individual_submissions(data)

    @safe_emit("room_submissions")
    def on_get_room_submissions(self, data):
        return service.get_room_submissions(data)
    
    @safe_emit("leader_changed")
    def on_set_leader(self, data):
        return service.set_leader(data)
    
    @safe_emit("user_kicked")
    def on_kick_user(self, data):
        return service.kick_user(data)