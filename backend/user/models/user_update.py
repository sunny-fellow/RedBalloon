from flask_restx import fields

def UserUpdateModel(api):
    """
    Define o modelo de dados para atualização de usuário.
    Este modelo é utilizado para validar requisições de atualização
    de perfil de usuário.
    """
    return api.model('UserUpdate', {
        'user_id': fields.Integer(required=True, description='ID do usuário', example=1),
        'name': fields.String(required=True, description="Nome do Usuário", example="João Silva"),
        'nickname': fields.String(required=True, description='Nickname/Login do usuário', example='joao_s'),
        'email': fields.String(required=True, description='Email do usuário', example='joao@gmail.com'),
        'password': fields.String(required=True, description='Senha do usuário', example='joj@123'),
        'avatar': fields.String(required=False, description="Avatar do usuário", example=""),
        'description': fields.String(required=False, description="Descrição/Bio do usuário", example="Olá, me chamo João!"),
        'nationality': fields.String(required=True, descriptiopn="Nacionalidade do usuário", example="BR"),
    })
