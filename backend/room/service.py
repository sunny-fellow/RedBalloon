from models.factories.sqlalchemy_factory import SQLAlchemyRepositoryFactory
from database.service import DatabaseService
from utils.singleton import Singleton
from utils.app_error import AppError
from datetime import datetime, timedelta, timezone
import uuid


@Singleton
class RoomService:
    def __init__(self):
        self.db_service = DatabaseService()
        factory = SQLAlchemyRepositoryFactory()
        self.repository = factory.create_room_repository()

    def list(self, query):
        def func(session):
            rooms = self.repository.list(
                session,
                query=query
            )

            return [
                {
                    "room_id": r.room_id,
                    "name": r.name,
                    "description": r.description,
                    "capacity": r.max_participants,
                    "current_players": r.current_players,
                    "ends_at": r.ends_at
                }
                for r in rooms
            ]

        return self.db_service.run(func)
    
    def create(self, data):
        def func(session):
            user_id = data["user_id"]

            # Calcular tempo
            ends_at = (
                datetime.now(timezone.utc) +
                timedelta(minutes=data["duration"])
            ).isoformat()
            data["ends_at"] = ends_at

            # Criar sala + socket
            room, room_socket = self.repository.create_room(session, data)

            # Adicionar criador + socket
            participant, user_socket = self.repository.add_participant(
                session,
                room.room_id,
                user_id,
                is_admin=True
            )

            # Processar problemas
            for item in data["problems"]:
                p_type = item["type"]
                points = item["points"]
                balloon = item["balloon_color"]

                # EXISTING
                if p_type == "EXISTING":
                    problem_id = item["existing_problem"]["problem_id"]

                # NEW
                elif p_type == "NEW":
                    p = item["new_problem"]
                    problem_data = {
                        "creator_id": user_id,
                        "title": p["title"],
                        "description": p["description"],
                        "time_limit": p["time_limit"],
                        "memory_limit": p["memory_limit"],
                        "validation_mode": p["validation_mode"],
                        "difficulty": p["difficulty"],
                        "private": True
                    }

                    problem = self.repository.create_problem(session, problem_data)
                    problem_id = problem.problem_id

                else:
                    raise AppError("Tipo de problema inválido")

                # Vincular à sala
                self.repository.add_problem_to_room(session, room.room_id, problem_id, points, balloon)

            return {
                "room_id": room.room_id,
                "room_socket": room_socket,
                "user_socket": user_socket
            }

        return self.db_service.run(func)
    
    def enter(self, data):
        def func(session):
            user_id = data["user_id"]
            room_id = data["room_id"]
            room_password = data.get("room_password")

            # Buscar sala
            room = self.repository.get_room_by_id(session, room_id)
            if not room:
                raise AppError("Sala não encontrada", 404)

            # Checar senha
            if room.password and room.password != (room_password or ""):
                raise AppError("Senha inválida")

            # Checar lotação
            current_players = self.repository.count_participants(session, room_id)
            if current_players >= room.max_participants:
                raise AppError("Sala cheia")

            # Adicionar participante
            participant, user_socket = self.repository.add_participant(
                session,
                room_id,
                user_id,
                is_admin=False
            )

            return {
                "room_id": room.room_id,
                "room_socket": room.socket,
                "user_socket": user_socket
            }

        return self.db_service.run(func)