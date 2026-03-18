from flask_restx import fields

def RegisterModel(api):
    return api.model("RegisterModel", {
        "name": fields.String(required=True, description="Nome do Usuário", example="João Silva"),
        'nickname': fields.String(required=True, description='Nickname do usuário', example='joao_s'),
        'email': fields.String(required=True, description='Email do usuário', example='joao@gmail.com'),
        'password': fields.String(required=True, description='Senha do usuário', example='joj@123'),
        'avatar': fields.String(required=False, description="Avatar do usuário", example=""),
        'description': fields.String(required=False, description="Descrição/Bio do usuário", example="Olá, me chamo João!"),
        'nationality': fields.String(required=True, descriptiopn="Nacionalidade do usuário", example="BR"),
    })