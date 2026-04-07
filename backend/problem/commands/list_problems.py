from utils.interfaces.command import Command
from problem.service import ProblemService

class ListProblemsCommand(Command):
    """
    Comando para listar problemas com filtros.
    """
    def __init__(self, service: ProblemService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.list(self.data)