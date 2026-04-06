# room/service.py (modificado com logger)
from models.factories.sqlalchemy_factory import SQLAlchemyRepositoryFactory
from database.service import DatabaseService
from utils.singleton import Singleton
from utils.app_error import AppError
from utils.adapter.json_logger_adapter import JsonLoggerAdapter
from datetime import datetime, timedelta, timezone
import uuid


@Singleton
class RoomService:
    def __init__(self):
        self.db_service = DatabaseService()
        factory = SQLAlchemyRepositoryFactory()
        self.repository = factory.create_room_repository()
        
        # Adapter para JSON logs
        self.logger = JsonLoggerAdapter(log_dir="logs", filename="room_actions.json")

    def list(self, query):
        def func(session):
            rooms = self.repository.list(
                session,
                query=query
            )

            result = [
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

            self.logger.debug(
                f"Listagem de salas realizada",
                context={
                    "query": query,
                    "result_count": len(result),
                    "action": "list_rooms"
                }
            )

            return result

        return self.db_service.run(func)
    
    def create(self, data):
        def func(session):
            user_id = data["user_id"]
            room_name = data.get("name", f"Sala de {user_id}")
            problem_count = len(data["problems"])

            # Calcular tempo
            ends_at = (
                datetime.now(timezone.utc) +
                timedelta(minutes=data["duration"])
            ).isoformat()
            data["ends_at"] = ends_at

            self.logger.info(
                f"Criando nova sala de competição",
                context={
                    "creator_id": user_id,
                    "room_name": room_name,
                    "duration": data["duration"],
                    "problem_count": problem_count,
                    "action": "create_room_start"
                }
            )

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
            problems_added = []
            for item in data["problems"]:
                p_type = item["type"]
                points = item["points"]
                balloon = item["balloon_color"]

                # EXISTING
                if p_type == "EXISTING":
                    problem_id = item["existing_problem"]["problem_id"]
                    problems_added.append({
                        "type": "EXISTING",
                        "problem_id": problem_id,
                        "points": points,
                        "balloon_color": balloon
                    })

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
                    
                    problems_added.append({
                        "type": "NEW",
                        "problem_id": problem_id,
                        "title": p["title"],
                        "points": points,
                        "balloon_color": balloon
                    })

                else:
                    self.logger.error(
                        f"Tipo de problema inválido ao criar sala",
                        context={
                            "creator_id": user_id,
                            "room_id": room.room_id,
                            "invalid_type": p_type,
                            "action": "create_room"
                        }
                    )
                    raise AppError("Tipo de problema inválido")

                # Vincular à sala
                self.repository.add_problem_to_room(session, room.room_id, problem_id, points, balloon)

            self.logger.info(
                f"Sala de competição criada com sucesso",
                context={
                    "room_id": room.room_id,
                    "room_socket": room_socket,
                    "creator_id": user_id,
                    "room_name": room_name,
                    "duration": data["duration"],
                    "ends_at": ends_at,
                    "problems_added": problems_added,
                    "action": "create_room_success"
                }
            )

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
                self.logger.warning(
                    f"Tentativa de entrar em sala inexistente",
                    context={
                        "user_id": user_id,
                        "room_id": room_id,
                        "action": "enter_room"
                    }
                )
                raise AppError("Sala não encontrada", 404)

            # Checar senha
            if room.password and room.password != (room_password or ""):
                self.logger.warning(
                    f"Tentativa de entrar em sala com senha inválida",
                    context={
                        "user_id": user_id,
                        "room_id": room_id,
                        "room_name": room.name,
                        "action": "enter_room"
                    }
                )
                raise AppError("Senha inválida")

            # Checar lotação
            current_players = self.repository.count_participants(session, room_id)
            if current_players >= room.max_participants:
                self.logger.warning(
                    f"Tentativa de entrar em sala lotada",
                    context={
                        "user_id": user_id,
                        "room_id": room_id,
                        "room_name": room.name,
                        "current_players": current_players,
                        "max_capacity": room.max_participants,
                        "action": "enter_room"
                    }
                )
                raise AppError("Sala cheia")

            # Adicionar participante
            participant, user_socket = self.repository.add_participant(
                session,
                room_id,
                user_id,
                is_admin=False
            )

            self.logger.info(
                f"Usuário entrou na sala de competição",
                context={
                    "room_id": room_id,
                    "user_id": user_id,
                    "room_name": room.name,
                    "current_players": current_players + 1,
                    "action": "enter_room_success"
                }
            )

            return {
                "room_id": room.room_id,
                "room_socket": room.socket,
                "user_socket": user_socket
            }

        return self.db_service.run(func)