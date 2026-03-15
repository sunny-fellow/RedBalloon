from utils.command import Command
from auth.service import AuthService

class RegisterCommand(Command):
    def __init__(self, service: AuthService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.register(self.data)