from flask_restx import Namespace, Resource
from utils.handle_exceptions import handle_exceptions
from message.service import MessageService

service = MessageService()

api = Namespace("message", description="")

# Models
from message.models.comment import CommentModel
from message.models.get_comments import GetCommentsModel

# Commands
from message.commands.comment import CommentCommand
from message.commands.get_comments import GetCommentsCommand

@api.route("/comment")
class Comment(Resource):

    @handle_exceptions
    @api.doc("Permite que o usuário comente em geral, em problemas ou em outras mensagens")
    @api.expect(CommentModel(api), validate = True)
    def post(self):
        data = api.payload
        command = CommentCommand(service, data)
        return command.execute(), 201
    
@api.route("/get_comments")
class GetComments(Resource):

    @handle_exceptions
    @api.doc("Consulta comentários do geral, de um problema ou de uma submissão")
    @api.expect(GetCommentsModel(api), validate = True)
    def get(self):
        data = api.payload
        command = GetCommentsCommand(service, data)
        return command.execute(), 200