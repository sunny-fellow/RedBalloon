from flask_restx import Namespace, Resource
from flask import request

from utils.handle_exceptions import handle_exceptions
from utils.get_user_id import get_user_id

from facade.facade_singleton_controller import FacadeSingletonController

# Models
from problem.models.create_problem import CreateProblemModel
from problem.models.problem_react import ProblemReactModel

api = Namespace("problem", description="Gerenciamento de Problemas")

facade = FacadeSingletonController()


@api.route("/create")
class CreateProblem(Resource):

    @handle_exceptions
    @api.expect(CreateProblemModel(api), validate=True)
    def post(self):
        data = api.payload
        return facade.create_problem(data), 201


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

        return facade.list_problems(query, tags), 200


@api.route("/<int:problem_id>")
class ProblemInfo(Resource):

    @handle_exceptions
    @api.doc("Retorna informações detalhadas de um problema específico")
    def get(self, problem_id):

        user_id = get_user_id()

        return facade.problem_info(problem_id, user_id), 200


@api.route("/react")
class ReactToProblem(Resource):

    @handle_exceptions
    @api.expect(ProblemReactModel(api), validate=True)
    @api.doc("Permite que o usuário dê like/dislike em um problema")
    def put(self):

        data = api.payload

        return facade.react_problem(data), 200

@api.route("/count")
class ProblemCount(Resource):

    @handle_exceptions
    @api.doc("Retorna o número total de problemas cadastrados")
    def get(self):
        return {
            "count": facade.count_problems()
        }, 200