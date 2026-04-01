from utils.command import Command
from ..service import UserService

class ListUsersCommand(Command):
    def __init__(self, service: UserService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.list_users(self.data)