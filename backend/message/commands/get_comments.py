from utils.interfaces.command import Command
from message.service import MessageService

class GetCommentsCommand(Command):
    def __init__(self, service: MessageService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.get_comments(self.data)