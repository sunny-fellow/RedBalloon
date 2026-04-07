from utils.interfaces.command import Command
from submission.service import SubmissionService

class ProblemSubmissionsCommand(Command):
    """
    Comando para listar todas as submissões ACEITAS de um problema específico.
    """
    def __init__(self, service: SubmissionService, problem_id: int):
        self.service = service
        self.problem_id = problem_id

    def execute(self):
        return self.service.problem_submissions(self.problem_id)