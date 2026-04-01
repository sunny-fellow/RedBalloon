from flask_restx import Namespace, Resource
from flask import request

from utils.handle_exceptions import handle_exceptions
from utils.get_user_id import get_user_id

from facade.facade_singleton_controller import FacadeSingletonController

# Models
from user.models.user_update import UserUpdateModel

api = Namespace('user', description='Gerenciamento de Usuários')

facade = FacadeSingletonController()

@api.route('/list')
class UserList(Resource):
    @handle_exceptions
    @api.doc("Endpoint de consulta de usuários para a tela /users da aplicação")
    @api.param("query", "Query de Busca por usuário")
    @api.param("country", "País de origem do usuário")
    def get(self):
        query = request.args.get("query")
        country = request.args.get("country")
        return facade.list_users(query, country), 200

@api.route('/details/<int:id_user>')
class UserDetails(Resource):
    @handle_exceptions
    def get(self, id_user):
        requester_id = get_user_id()
        result = facade.user_details(id_user, requester_id)
        return result, 200

@api.route('/follow/<int:id_user>')
class UserFollow(Resource):
    @handle_exceptions
    def get(self, id_user):
        follower_id = get_user_id()
        return facade.follow_user(follower_id, id_user), 200

@api.route('/delete/<int:id_user>')
class UserDelete(Resource):
    @handle_exceptions
    def delete(self, id_user):
        result = facade.delete_user(id_user)

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
        updated_user = facade.update_user(data.get("user_id"), data)

        if not updated_user:
            return {"message": "Usuário não encontrado"}, 404

        return updated_user, 200
    
@api.route('/count')
class UserCount(Resource):
    @handle_exceptions
    @api.doc("Retorna o número total de usuários cadastrados")
    def get(self):
        return {
            "count": facade.count_users()
        }, 200