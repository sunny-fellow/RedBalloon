from flask_restx import Namespace, Resource
from utils.handle_exceptions import handle_exceptions
from auth.service import AuthService

service = AuthService()

api = Namespace("auth", description="Operações de Autenticação")

# Models
from auth.models.login import LoginModel
from auth.models.register import RegisterModel

# Commands
from auth.commands.login import LoginCommand
from auth.commands.register import RegisterCommand

@api.route("/login")
@api.doc(description="Endpoint pelo qual o usuário faz login e recebe JWT")
class AuthLogin(Resource):

    @handle_exceptions
    @api.expect(LoginModel(api))
    def post(self):
        data = api.payload
        command = LoginCommand(service, data)
        return command.execute(), 200
    

@api.route("/register")
@api.doc(description="Endpoint de criação de usuário")
class AuthRegister(Resource):
    @handle_exceptions
    @api.expect(RegisterModel(api))
    def post(self):
        data = api.payload
        command = RegisterCommand(service, data)
        return command.execute(), 201
    
