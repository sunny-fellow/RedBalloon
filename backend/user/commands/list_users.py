from utils.command import Command
from ..service import UserService

class ListUsersCommand(Command):

    def __init__(self, service: UserService):
        self.service = service

    def execute(self):
        return self.service.list_users()