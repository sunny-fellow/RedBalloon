from flask_restx import fields

# Modelo de input para os endpoints (somente senha admin)
def getPasswordModel(api):
    return api.model("AdminPassword", {
        "password": fields.String(required=True, description="Senha de administrador")
    })