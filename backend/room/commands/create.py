from utils.interfaces.command import Command
from room.service import RoomService

class CreateRoomCommand(Command):
    """
    Comando para criação de uma nova sala de competição.
    """
    def __init__(self, service: RoomService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.create(self.data)