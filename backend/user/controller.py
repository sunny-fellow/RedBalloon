from flask_restx import Namespace, Resource
from user.service import UserService, ValidationError
from user.models import *
import traceback

api = Namespace('user', description='Gerenciamento de Usuários')
service = UserService()  # O arquivo padrão será o 'users.json'

@api.route('/list')
class UserList(Resource):
    def get(self):
        """Lista todos os usuários"""
        try:
            return service.list_users(), 200
        
        except Exception as e:
            return {'message': f'Erro interno no servidor: {str(e)}'}, 500

@api.route('/create')
class UserCreate(Resource):
    @api.expect(getUserModel(api))
    def post(self):
        """Cria um novo usuário"""
        data = api.payload
        try:
            new_user = service.create_user(data)
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
        """Deleta um usuário pelo ID"""
        try:
            result = service.delete_user(id_user)
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
        """Atualiza um usuário existente"""
        try:
            updated_user = service.update_user(api.payload.get('id'), api.payload)
            if not updated_user:
                return {"message": "Usuário não encontrado"}, 404    
            
            return updated_user, 200
        
        except ValidationError as e:
            return {'message': str(e)}, 400
        
        except IOError as e:
            return {'message': f'Erro de armazenamento: {str(e)}'}, 500
        
        except Exception as e:
            return {'message': f'Erro interno inesperado: {str(e)}'}, 500