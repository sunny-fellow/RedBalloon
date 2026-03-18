from flask_restx import Namespace, Resource
from flask import request
from utils.handle_exceptions import handle_exceptions
from utils.get_user_id import get_user_id
from problem.service import ProblemService

service = ProblemService()

api = Namespace("problem", description="Gerenciamento de Problemas")

# Models
from problem.models.create_problem import CreateProblemModel
from problem.models.problem_react import ProblemReactModel

# Commands
from problem.commands.create_problem import CreateProblemCommand
from problem.commands.list_problems import ListProblemsCommand
from problem.commands.problem_info import ProblemInfoCommand
from problem.commands.problem_react import ProblemReactCommand

@api.route("/create")
class CreateProblem(Resource):

    @handle_exceptions
    @api.expect(CreateProblemModel(api), validate = True)
    def post(self):
        data = api.payload

        command = CreateProblemCommand(service, data)
        return command.execute(), 201
    
@api.route("/list")
class ListProblems(Resource):

    @handle_exceptions
    @api.doc("Endpoint de busca de problemas, podendo passar querys e tags opcionais")
    @api.param("query", "Texto de Busca")
    @api.param("tags", "Tags do Problema")
    def get(self):
        query = request.args.get("query")
        tags = request.args.get("tags")

        if tags:
            tags = tags.split(",")

        command = ListProblemsCommand(service, {"query": query, "tags": tags})
        return command.execute(), 200
    
@api.route("/<int:problem_id>")
class ProblemInfo(Resource):

    @handle_exceptions
    @api.param("problem_id", "ID do Problema a ser buscado")
    @api.doc("Retorna informações detalhadas de um problema específico")
    def get(self, problem_id):
        user_id = get_user_id()
        command = ProblemInfoCommand(service, {"problem_id": problem_id, "user_id": user_id})
        return command.execute(), 200
    
@api.route("/react")
class ReactToProblem(Resource):

    @handle_exceptions
    @api.expect(ProblemReactModel(api), validate = True)
    @api.doc("Permite que o usuário dê like/dislike em um problema")
    def put(self):
        data = api.payload
        command = ProblemReactCommand(service, data)
        return command.execute(), 200