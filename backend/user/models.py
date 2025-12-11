from flask_restx import fields, Model

def getUserModel(api):
    return api.model('User', {
        'name': fields.String(required=True, description='Nome do usuário', example='João'),
        'email': fields.String(required=True, description='Email do usuário', example='joao@gmail.com'),
        'login': fields.String(required=True, description='Login do usuário', example='joj'),
        'password': fields.String(required=True, description='Senha do usuário', example='joj@123'),
        'is_mod': fields.Boolean(required=False, default=False, description='Se é moderador')
    })

def getUserUpdateModel(api):
    return api.model('UserUpdate', {
        'id': fields.Integer(required=True, description='ID do usuário', example=1),
        'name': fields.String(required=False, description='Nome do usuário', example='João'),
        'email': fields.String(required=False, description='Email do usuário', example='joao@email.com'),
        'login': fields.String(required=False, description='Login do usuário', example='joao123'),
        'password': fields.String(required=False, description='Senha do usuário', example='senha123'),
        'is_mod': fields.Boolean(required=False, default=False, description='Se é moderador')
    })