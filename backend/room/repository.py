from sqlalchemy import func, and_
from sqlalchemy.orm import aliased
import uuid

from models.user.user import User
from models.room.room import Room
from models.problem.problem import Problem
from models.room.room_participant import RoomParticipant
from models.room.room_problem import RoomProblem
from models.room.room_chat import RoomChat
from models.room.room_submission import RoomSubmission


class RoomRepository:

    def list(self, session, query=None):
        creator = aliased(User)
        creator_participant = aliased(RoomParticipant)

        q = session.query(
            Room.room_id,
            Room.name,
            Room.description,
            Room.max_participants,
            Room.ends_at,

            func.count(RoomParticipant.user_id).label("current_players"),

            creator.name.label("creator_name")
        ).outerjoin(
            RoomParticipant,
            RoomParticipant.room_id == Room.room_id
        ).outerjoin(
            creator_participant,
            and_(
                creator_participant.room_id == Room.room_id,
                creator_participant.is_admin == True
            )
        ).outerjoin(
            creator,
            creator.user_id == creator_participant.user_id
        )

        if query:
            q = q.filter(Room.name.ilike(f"%{query}%"))

        q = q.group_by(
            Room.room_id,
            creator.name
        ).limit(50)

        return q.all()
    
    def create_room(self, session, data):
        room_socket = str(uuid.uuid4())  # socket da sala
        room = Room(
            name=data["room_name"],
            description=data.get("room_description", ""),
            password=data.get("room_password"),
            max_participants=data["capacity"],
            ends_at=data["ends_at"],
            socket=room_socket
        )
        session.add(room)
        session.flush()  # pega room_id
        return room, room_socket

    def add_participant(self, session, room_id, user_id, is_admin=False):
        user_socket = str(uuid.uuid4())  # socket do participante
        participant = RoomParticipant(
            room_id=room_id,
            user_id=user_id,
            is_admin=is_admin,
            socket=user_socket
        )
        session.add(participant)
        return participant, user_socket

    # -------- PROBLEM --------
    def create_problem(self, session, data):
        problem = Problem(**data)
        session.add(problem)
        session.flush()
        return problem

    # -------- ROOM_PROBLEM --------
    def add_problem_to_room(self, session, room_id, problem_id, points, balloon):
        rp = RoomProblem(
            room_id=room_id,
            problem_id=problem_id,
            points = points,
            balloon = balloon
        )
        session.add(rp)

    def get_room_by_id(self, session, room_id):
        return session.query(Room).filter(Room.room_id == room_id).first()

    def count_participants(self, session, room_id):
        return session.query(RoomParticipant).filter(
            RoomParticipant.room_id == room_id
        ).count()