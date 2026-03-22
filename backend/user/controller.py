from flask_restx import Namespace, Resource
from flask import request
from user.service import UserService
from utils.handle_exceptions import handle_exceptions
from utils.get_user_id import get_user_id

# Commands
from user.commands.delete_user import DeleteUserCommand
from user.commands.list_users import ListUsersCommand
from user.commands.update_user import UpdateUserCommand
from user.commands.user_details import UserDetailsCommand
from user.commands.user_follow import UserFollowCommand

# Models
from user.models.user_update import UserUpdateModel

import traceback

api = Namespace('user', description='Gerenciamento de Usuários')
service = UserService()

@api.route('/list')
class UserList(Resource):

    @handle_exceptions
    @api.doc("Endpoint de consulta de usuários para a tela /users da aplicação")
    @api.param("query", "Query de Busca por usuário")
    @api.param("country", "País de origem do usuário")
    def get(self):
        query = request.args.get("query")
        country = request.args.get("country")

        command = ListUsersCommand(service, {"query": query, "country": country})
        return command.execute(), 200

@api.route('/<int:user_id>')
class UserDetails(Resource):

    @handle_exceptions
    @api.param("user_id", "ID do usuário que está sendo buscado")
    def get(self, user_id):
        requester_id = get_user_id()
        command = UserDetailsCommand(service, {
            "user_id": user_id,
            "requester_id": requester_id
        })
        return command.execute(), 200
    
@api.route('/follow/<int:user_id>')
class UserFollow(Resource):

    @handle_exceptions
    @api.param("user_id", "ID do usuário a dar follow ou unfollow")
    def get(self, user_id):
        follower_id = get_user_id()
        command = UserFollowCommand(service, {
            "follower_id": follower_id,
            "following_id": user_id
        })
        return command.execute(), 200


@api.route('/delete/<int:id_user>')
class UserDelete(Resource):

    @handle_exceptions
    def delete(self, id_user):
        command = DeleteUserCommand(service, id_user)
        result = command.execute()

        if result:
            return {'message': 'Usuário deletado com sucesso'}, 200
        else:
            return {'message': 'Usuário não encontrado'}, 404


@api.route('/update')
class UserUpdate(Resource):

    @handle_exceptions
    @api.expect(UserUpdateModel(api), validate=True)
    def put(self):

        data = api.payload

        command = UpdateUserCommand(service, data.get("user_id"), data)
        updated_user = command.execute()

        if not updated_user:
            return {"message": "Usuário não encontrado"}, 404

        return updated_user, 200