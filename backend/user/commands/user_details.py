from utils.command import Command
from user.service import UserService

class UserDetailsCommand(Command):

    def __init__(self, service: UserService, data):
        self.service = service
        self.data = data

    def execute(self):

        result = self.service.get_user(self.data)

        return result