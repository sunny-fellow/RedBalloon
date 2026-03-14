from utils.command import Command
from user.service import UserService

class CreateUserCommand(Command):

    def __init__(self, service: UserService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.create_user(self.data)