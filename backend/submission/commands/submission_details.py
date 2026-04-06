from utils.interfaces.command import Command
from submission.service import SubmissionService

class SubmissionDetailsCommand(Command):
    def __init__(self, service: SubmissionService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.details(self.data)