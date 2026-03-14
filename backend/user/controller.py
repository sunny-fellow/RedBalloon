from flask_restx import Namespace, Resource
from user.service import UserService, ValidationError
from user.models import *

from .commands.create_user import CreateUserCommand
from .commands.delete_user import DeleteUserCommand
from .commands.list_users import ListUsersCommand
from .commands.update_user import UpdateUserCommand

import traceback

api = Namespace('user', description='Gerenciamento de Usuários')
service = UserService()

@api.route('/list')
class UserList(Resource):

    def get(self):
        try:
            command = ListUsersCommand(service)
            return command.execute(), 200

        except Exception as e:
            return {'message': f'Erro interno no servidor: {str(e)}'}, 500


@api.route('/create')
class UserCreate(Resource):

    @api.expect(getUserModel(api))
    def post(self):

        data = api.payload

        try:
            command = CreateUserCommand(service, data)
            new_user = command.execute()

            return new_user, 201

        except ValidationError as e:
            return {'message': str(e)}, 400

        except IOError as e:
            return {'message': f'Erro de armazenamento: {str(e)}'}, 500

        except Exception as e:
            traceback.print_exc()
            return {'message': f'Erro interno inesperado: {str(e)}'}, 500


@api.route('/delete/<int:id_user>')
class UserDelete(Resource):

    def delete(self, id_user):

        try:
            command = DeleteUserCommand(service, id_user)

            result = command.execute()

            if result:
                return {'message': 'Usuário deletado com sucesso'}, 200
            else:
                return {'message': 'Usuário não encontrado'}, 404

        except IOError as e:
            return {'message': f'Erro de armazenamento: {str(e)}'}, 500

        except Exception as e:
            return {'message': f'Erro interno inesperado: {str(e)}'}, 500


@api.route('/update')
class UserUpdate(Resource):

    @api.expect(getUserUpdateModel(api))
    def put(self):

        data = api.payload

        try:
            command = UpdateUserCommand(service, data.get("user_id"), data)

            updated_user = command.execute()

            if not updated_user:
                return {"message": "Usuário não encontrado"}, 404

            return updated_user, 200

        except ValidationError as e:
            return {'message': str(e)}, 400

        except IOError as e:
            return {'message': f'Erro de armazenamento: {str(e)}'}, 500

        except Exception as e:
            return {'message': f'Erro interno inesperado: {str(e)}'}, 500