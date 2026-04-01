from utils.command import Command
from ..service import UserService

class DeleteUserCommand(Command):
    def __init__(self, service: UserService, user_id):
        self.service = service
        self.user_id = user_id

    def execute(self):
        return self.service.delete_user(self.user_id)