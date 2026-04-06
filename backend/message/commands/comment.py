from utils.interfaces.command import Command
from message.service import MessageService

class CommentCommand(Command):
    def __init__(self, service: MessageService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.comment(self.data)