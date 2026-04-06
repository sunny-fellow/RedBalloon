from flask_restx import Namespace, Resource
from utils.handle_exceptions import handle_exceptions
from auth.service import AuthService

from auth.models.login import LoginModel
from auth.models.register import RegisterModel

from auth.commands.login import LoginCommand
from auth.commands.register import RegisterCommand

service = AuthService()
api = Namespace("auth", description="Operações de Autenticação")

@api.route("/login")
class AuthLogin(Resource):
    @api.doc(description="Endpoint pelo qual o usuário faz login e recebe JWT")
    @handle_exceptions
    @api.expect(LoginModel(api))
    def post(self):
        data = api.payload
        command = LoginCommand(service, data)
        return command.execute(), 200
    
@api.route("/register")
class AuthRegister(Resource):
    @api.doc(description="Endpoint de criação de usuário")
    @handle_exceptions
    @api.expect(RegisterModel(api))
    def post(self):
        data = api.payload
        command = RegisterCommand(service, data)
        return command.execute(), 201
    
