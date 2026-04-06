from utils.interfaces.command import Command
from auth.service import AuthService

class LoginCommand(Command):
    def __init__(self, service: AuthService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.login(self.data)