from database.service import DatabaseService
from utils.singleton import Singleton
from utils.app_error import AppError

from models.room.room import Room
from models.room.room_participant import RoomParticipant
from models.room.room_chat import RoomChat
from models.room.room_problem import RoomProblem
from models.room.room_submission import RoomSubmission
from models.problem.problem import Problem
from models.user.user import User

@Singleton
class RoomGatewayRepository:
    """
    Repositório para operações de banco de dados do gateway de salas.
    Gerencia acesso a dados para chat, submissões, participantes,
    problemas e configurações de sala via WebSocket.
    """
    def __init__(self):
        self.db_service = DatabaseService()

    def get_room_by_id(self, room_id: int):
        def func(session):
            return session.query(Room).filter(Room.room_id == room_id).first()
        return self.db_service.run(func)

    def get_participant(self, room_id: int, user_id: int):
        def func(session):
            return session.query(RoomParticipant).filter(
                RoomParticipant.room_id == room_id,
                RoomParticipant.user_id == user_id
            ).first()
        return self.db_service.run(func)

    def update_room_config(self, room_id: int, new_config: dict):
        def func(session):
            room = session.query(Room).filter(Room.room_id == room_id).first()
            if not room:
                raise AppError("Sala não encontrada")
            for key, value in new_config.items():
                if hasattr(room, key):
                    setattr(room, key, value)
            session.commit()
            return room
        return self.db_service.run(func)

    def add_message(self, room_id: int, user_id: int, message: str):
        def func(session):
            msg = RoomChat(room_id=room_id, user_id=user_id, message=message)
            session.add(msg)
            session.commit()
            session.refresh(msg)
            return {
                "message_id": msg.message_id,
                "room_id": room_id,
                "user_id": user_id,
                "message": message,
                "sent_at": msg.sent_at
            }
        return self.db_service.run(func)

    # Problemas da sala
    def get_problems_for_room(self, room_id: int):
        def func(session):
            problems = session.query(
                RoomProblem.room_id,
                RoomProblem.problem_id,
                RoomProblem.points,
                RoomProblem.balloon_color,
                Problem.title,
                Problem.description,
                Problem.difficulty
            ).join(Problem, Problem.problem_id == RoomProblem.problem_id
            ).filter(RoomProblem.room_id == room_id).all()
            return [
                {
                    "problem_id": p.problem_id,
                    "title": p.title,
                    "description": p.description,
                    "difficulty": p.difficulty,
                    "points": p.points,
                    "balloon_color": p.balloon_color
                } for p in problems
            ]
        return self.db_service.run(func)

    def get_problem_details(self, room_id: int, problem_id: int):
        def func(session):
            rp = session.query(RoomProblem).filter(
                RoomProblem.room_id == room_id,
                RoomProblem.problem_id == problem_id
            ).first()
            if not rp:
                raise AppError("Problema não encontrado na sala")
            problem = session.query(Problem).filter(Problem.problem_id == problem_id).first()
            return {
                "problem_id": problem.problem_id,
                "title": problem.title,
                "description": problem.description,
                "time_limit": problem.time_limit,
                "memory_limit": problem.memory_limit,
                "difficulty": problem.difficulty,
                "points": rp.points,
                "balloon_color": rp.balloon_color
            }
        return self.db_service.run(func)

    # Submissões
    def create_room_submission(self, data: dict):
        def func(session):
            # Cria nova submissão com status JUDGING
            submission = RoomSubmission(
                room_id=data["room_id"],
                user_id=data["user_id"],
                problem_id=data["problem_id"],
                code=data["code"],
                language=data["language"],
                time_taken=0,
                status="JUDGING"
            )
            session.add(submission)
            session.commit()
            session.refresh(submission)
            return submission
        return self.db_service.run(func)

    def judge_room_submission(self, submission: RoomSubmission):
        # Executa código do usuário
        result = self.execution_service.run(
            problem_id=submission.problem_id,
            source_code=submission.code,
            language=submission.language.value
        )

        # Atualiza somente esta submissão
        def _update(session):
            # Pega exatamente o objeto que já temos
            sub = session.merge(submission)
            sub.status = result["status"]
            sub.time_taken = result.get("time_spent", 0)
            session.commit()
            session.refresh(sub)
            return sub

        updated_submission = self.db_service.run(_update)

        return {
            "submission_id": updated_submission.problem_id,
            "status": updated_submission.status,
            "time_taken": updated_submission.time_taken,
            "user_id": updated_submission.user_id,
            "room_id": updated_submission.room_id
        }

    def get_user_submissions(self, room_id: int, user_id: int):
        def func(session):
            subs = session.query(RoomSubmission).filter(
                RoomSubmission.room_id == room_id,
                RoomSubmission.user_id == user_id
            ).all()
            return [
                {
                    "problem_id": s.problem_id,
                    "status": s.status,
                    "submitted_at": s.submitted_at,
                    "time_taken": s.time_taken
                } for s in subs
            ]
        return self.db_service.run(func)

    def get_all_room_submissions(self, room_id: int):
        def func(session):
            subs = session.query(RoomSubmission).filter(
                RoomSubmission.room_id == room_id
            ).all()
            return [
                {
                    "problem_id": s.problem_id,
                    "user_id": s.user_id,
                    "status": s.status,
                    "submitted_at": s.submitted_at,
                    "time_taken": s.time_taken
                } for s in subs
            ]
        return self.db_service.run(func)

    # Informação da sala
    def get_lobby_info(self, room_id: int):
        def func(session):
            # Pega a sala
            room = session.query(Room).filter(Room.room_id == room_id).first()
            
            if not room:
                raise AppError("Sala não encontrada")

            # Pega participantes com info do usuário
            participants_query = (
                session.query(RoomParticipant, User)
                .join(User, RoomParticipant.user_id == User.user_id)
                .filter(RoomParticipant.room_id == room_id)
                .order_by(RoomParticipant.score.desc())  # ordena pelos pontos
            )

            participants = [
                {
                    "user_id": p.RoomParticipant.user_id,
                    "avatar": p.User.avatar,
                    "name": p.User.name,
                    "score": p.RoomParticipant.score,
                    "is_admin": p.RoomParticipant.is_admin
                }
                for p in participants_query.all()
            ]
            current_players = len(participants)

            return {
                "room_id": room.room_id,
                "name": room.name,
                "description": room.description,
                "creator_name": room.creator.name,
                "current_players": current_players,
                "max_players": room.max_participants,
                "participants": participants
            }

        return self.db_service.run(func)
    
    def is_admin(self, room_id: int, user_id: int) -> bool:
        def func(session):
            participant = session.query(RoomParticipant).filter_by(
                room_id=room_id,
                user_id=user_id
            ).first()
            
            if not participant:
                raise AppError("Usuário não participa da sala")
            
            return participant.is_admin
        return self.db_service.run(func)

    def set_leader(self, room_id: int, new_leader_id: int):
        def func(session):
            # Limpa o leader atual
            session.query(RoomParticipant).filter_by(room_id=room_id).update({"is_admin": False})
            # Seta o novo líder
            participant = session.query(RoomParticipant).filter_by(
                room_id=room_id,
                user_id=new_leader_id
            ).first()
            
            if not participant:
                raise AppError("Usuário a ser definido como líder não está na sala")
            
            participant.is_admin = True
            session.commit()
            
            return participant
        return self.db_service.run(func)

    def remove_participant(self, room_id: int, user_id: int):
        def func(session):
            participant = session.query(RoomParticipant).filter_by(
                room_id=room_id,
                user_id=user_id
            ).first()
            
            if not participant:
                raise AppError("Usuário não encontrado na sala")
            
            session.delete(participant)
            session.commit()
            
            return participant
        return self.db_service.run(func)