from flask_restx import Namespace, Resource
from user.service import UserService
from user.models import *

api = Namespace('user', description='Gerenciamento de Usuários')
service = UserService()

@api.route('/list')
class UserList(Resource):
    def get(self):
        """Lista todos os usuários"""
        return service.list_users(), 200

@api.route('/create')
class UserCreate(Resource):
    @api.expect(getUserModel(api))
    def post(self):
        """Cria um novo usuário"""
        data = api.payload  # JSON enviado
        new_user = service.create_user(data)
        return new_user, 201
    
@api.route('/delete/<int:id_user>')
class UserDelete(Resource):
    def delete(self, id_user):
        """Deleta um usuário pelo ID"""
        result = service.delete_user(id_user)
        if result:
            return {'message': 'Usuário deletado com sucesso'}, 200
        else:
            return {'message': 'Usuário não encontrado'}, 404
        
@api.route('/update')
class UserUpdate(Resource):
    @api.expect(getUserUpdateModel(api))
    def put(self):
        updated_user = service.update_user(api.payload.get('id'), api.payload)
        if not updated_user:
            return {"message": "Usuário não encontrado"}, 404
        return updated_user, 200
