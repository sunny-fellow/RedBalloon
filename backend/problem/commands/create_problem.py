from utils.command import Command
from problem.service import ProblemService

class CreateProblemCommand(Command):
    def __init__(self, service: ProblemService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.create_problem(self.data)