from utils.interfaces.command import Command
from problem.service import ProblemService

class ProblemInfoCommand(Command):
    def __init__(self, service: ProblemService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.problem_info(self.data)