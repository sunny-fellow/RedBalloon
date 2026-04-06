from utils.interfaces.command import Command
from problem.service import ProblemService

class ProblemReactCommand(Command):
    def __init__(self, service: ProblemService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.problem_react(self.data)