from .command import Command

class DeleteUserCommand(Command):

    def __init__(self, service, user_id):
        self.service = service
        self.user_id = user_id

    def execute(self):
        return self.service.delete_user(self.user_id)