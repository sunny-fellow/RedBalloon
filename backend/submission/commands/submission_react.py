from utils.interfaces.command import Command
from submission.service import SubmissionService

class SubmissionReactCommand(Command):
    """
    Comando para registrar uma reação (like/dislike) em uma submissão.
    """
    def __init__(self, service: SubmissionService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.react(self.data)