from .command import Command

class CreateUserCommand(Command):

    def __init__(self, service, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.create_user(self.data)