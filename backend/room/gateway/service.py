# room/gateway/service.py
from datetime import datetime, timezone
from functools import wraps
from utils.singleton import Singleton
from utils.app_error import AppError
from room.gateway.repository import RoomGatewayRepository

@Singleton
class RoomGatewayService:
    def __init__(self):
        self.repository = RoomGatewayRepository()

    def validate_sockets(func):
        @wraps(func)
        def wrapper(self, data: dict, *args, **kwargs):
            # campos obrigatórios
            required_keys = ["user_id", "room_id", "user_socket", "room_socket"]
            for key in required_keys:
                if key not in data:
                    raise AppError(f"{key} é obrigatório")

            # valida se sala existe
            room = self.repository.get_room_by_id(data["room_id"])
            if not room:
                raise AppError("Sala não encontrada")

            # valida se usuário participa da sala
            participant = self.repository.get_participant(data["room_id"], data["user_id"])
            if not participant:
                raise AppError("Usuário não participa da sala")

            # se tudo ok, chama o método original
            return func(self, data, *args, **kwargs)
        return wrapper


    # ---------------- chat ----------------
    @validate_sockets
    def send_message(self, data: dict):
        """
            data: {room_id, user_id, message, user_socket}
        """
        if not data.get("message"):
            raise AppError("Mensagem vazia")

        msg = self.repository.add_message(
            room_id=data["room_id"],
            user_id=data["user_id"],
            message=data["message"]
        )

        return msg

    # ---------------- submissões ----------------
    @validate_sockets
    def submit_problem(self, data: dict):
        """
        Cria uma submissão nova na sala, julga e retorna resultado.
        data: {
            user_id, room_id, problem_id, code, language, user_socket, room_socket
        }
        """
        # validações básicas
        user_id = data.get("user_id")
        room_id = data.get("room_id")
        problem_id = data.get("problem_id")
        code = data.get("code")
        language = data.get("language")

        if not all([user_id, room_id, problem_id, code, language]):
            raise AppError("Parâmetros inválidos para submissão")

        submission = self.repository.create_room_submission(data)
        result = self.repository.judge_room_submission(submission)

        return result

    # ---------------- configuração da sala ----------------
    @validate_sockets
    def update_room_config(self, data: dict):
        """
        data: {room_id, user_id, new_config}
        """
        # verifica se user é admin
        room = self.repository.get_room_by_id(data["room_id"])
        participant = self.repository.get_participant(data["room_id"], data["user_id"])
        if not participant or not participant.is_admin:
            raise AppError("Usuário não é administrador da sala")

        updated_room = self.repository.update_room_config(data["room_id"], data["new_config"])
        return updated_room

    # ---------------- problemas da sala ----------------
    @validate_sockets
    def get_room_problems(self, room_id: int):
        """
        Retorna lista de problemas da sala com id, title, difficulty, points, balloon_color
        """
        return self.repository.get_problems_for_room(room_id)

    @validate_sockets
    def get_problem_details(self, data: dict):
        """
        Retorna detalhes de um problema específico da sala
        data: {room_id, problem_id}
        """
        return self.repository.get_problem_details(data["room_id"], data["problem_id"])

    # ---------------- info da sala ----------------
    @validate_sockets
    def get_room_lobby_info(self, data: dict):
        """
        Retorna informações gerais da sala (players, ranking, status)
        data: {room_id}
        """
        return self.repository.get_lobby_info(data["room_id"])

    @validate_sockets
    def get_individual_submissions(self, data: dict):
        """
        Retorna as submissões de um usuário na sala
        data: {room_id, user_id}
        """
        return self.repository.get_user_submissions(data["room_id"], data["user_id"])

    @validate_sockets
    def get_room_submissions(self, data: dict):
        """
        Retorna todas as submissões da sala (para ranking)
        data: {room_id}
        """
        return self.repository.get_all_room_submissions(data["room_id"])
    
    
    @validate_sockets
    def set_leader(self, data: dict):
        self._validate_data(data)

        user_id_to_set = data.get("new_leader_id")
        if not user_id_to_set:
            raise AppError("new_leader_id não fornecido")

        # Verifica se quem está solicitando é admin
        if not self.repo.is_admin(data["room_id"], data["user_id"]):
            raise AppError("Somente o admin pode definir um novo líder")

        # Atualiza no banco de dados
        self.repo.set_leader(data["room_id"], user_id_to_set)
        return {"new_leader_id": user_id_to_set}

    
    @validate_sockets
    def kick_user(self, data: dict):
        self._validate_data(data)

        user_id_to_kick = data.get("kick_user_id")
        if not user_id_to_kick:
            raise AppError("kick_user_id não fornecido")

        # Verifica se quem está solicitando é admin
        if not self.repo.is_admin(data["room_id"], data["user_id"]):
            raise AppError("Somente o admin pode expulsar usuários")

        if user_id_to_kick == data["user_id"]:
            raise AppError("O admin não pode se expulsar")

        # Remove o usuário da sala no banco
        self.repo.remove_participant(data["room_id"], user_id_to_kick)
        return {"kicked_user_id": user_id_to_kick}