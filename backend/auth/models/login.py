from flask_restx import fields

def LoginModel(api):
    return api.model("LoginModel", {
        "login": fields.String(required=True, description="nickname ou e-mail", example="joao_s@gmail.com"),
        "password": fields.String(required=True, description="senha de usuário", example="joao123")
    })