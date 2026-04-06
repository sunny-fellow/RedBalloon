from utils.interfaces.command import Command
from user.service import UserService

class UserFollowCommand(Command):
    def __init__(self, service: UserService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.follow(self.data)