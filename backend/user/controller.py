from flask_restx import Namespace, Resource
from user.service import UserService
from utils.handle_exceptions import handle_exceptions

# Commands
from user.commands.delete_user import DeleteUserCommand
from user.commands.list_users import ListUsersCommand
from user.commands.update_user import UpdateUserCommand

# Models
from user.models.user_update import UserUpdateModel

import traceback

api = Namespace('user', description='Gerenciamento de Usuários')
service = UserService()

@api.route('/list')
class UserList(Resource):

    @handle_exceptions
    def get(self):
        command = ListUsersCommand(service)
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