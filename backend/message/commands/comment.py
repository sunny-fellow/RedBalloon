from utils.interfaces.command import Command
from message.service import MessageService

class CommentCommand(Command):
    """
    Comando para adicionar um comentário em uma mensagem ou entidade.
    """
    def __init__(self, service: MessageService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.comment(self.data)