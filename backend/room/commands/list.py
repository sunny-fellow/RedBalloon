from utils.command import Command
from room.service import RoomService

class ListRoomCommand(Command):
    def __init__(self, service: RoomService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.list(self.data)