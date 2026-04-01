from flask_restx import Namespace, Resource
from utils.handle_exceptions import handle_exceptions
from utils.get_user_id import get_user_id
from submission.service import SubmissionService

service = SubmissionService()

api = Namespace("submission", description="Gerenciamento de Submissões")

# Models
from submission.models.submit import SubmissionModel
from submission.models.submission_react import SubmissionReactModel

# Commands
from submission.commands.submit import SubmissionCommand
from submission.commands.problem_submissions import ProblemSubmissionsCommand
from submission.commands.submission_react import SubmissionReactCommand
from submission.commands.submission_details import SubmissionDetailsCommand

@api.route("/submit")
class Submit(Resource):
    @handle_exceptions
    @api.doc("Endpoint de submissão para problemas públicos")
    @api.expect(SubmissionModel(api), validate = True)
    def post(self):
        data = api.payload
        command = SubmissionCommand(service, data)
        return command.execute(), 201
    
@api.route("/problem/<int:problem_id>")
class ProblemSubmissions(Resource):
    @handle_exceptions
    @api.doc("Retorna todas as submissões ACEITAS feitas a um problema específico")
    @api.param("problem_id", "ID do Problema ao qual as submissões pertencem")
    def get(self, problem_id):
        command = ProblemSubmissionsCommand(service, problem_id)
        return command.execute(), 200
    
@api.route("/<int:submission_id>")
class SubmissionDetails(Resource):
    @handle_exceptions
    @api.doc("Retorna informações detalhadas da submissão buscada")
    @api.param("submission_id", "ID da Submissão a ser buscada")
    def get(self, submission_id):
        command = SubmissionDetailsCommand(
            service, 
            {
                "submission_id": submission_id, 
                "user_id": get_user_id()
            }
        )
        return command.execute(), 200

@api.route("/react")
class SubmissionReact(Resource):
    @handle_exceptions
    @api.expect(SubmissionReactModel(api), validate = True)
    @api.doc("Permite que usuários dêem likes/dislikes em submissões")
    def put(self):
        data = api.payload
        command = SubmissionReactCommand(service, data)
        return command.execute(), 200