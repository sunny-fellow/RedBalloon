from .command import Command

class ListUsersCommand(Command):

    def __init__(self, service):
        self.service = service

    def execute(self):
        return self.service.list_users()