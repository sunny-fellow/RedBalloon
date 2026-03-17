from flask_restx import Namespace, Resource
from utils.handle_exceptions import handle_exceptions
from problem.service import ProblemService

service = ProblemService()

api = Namespace("problem", description="Gerenciamento de Problemas")

# Models
from problem.models.create_problem import CreateProblemModel

# Commands
from problem.commands.create_problem import CreateProblemCommand

@api.route("/create")
class CreateProblem(Resource):

    @handle_exceptions
    @api.expect(CreateProblemModel(api), validate = True)
    def post(self):
        data = api.payload

        command = CreateProblemCommand(service, data)
        return command.execute(), 201