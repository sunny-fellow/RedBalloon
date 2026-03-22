from flask_restx import fields

def EnterRoomModel(api):
    return api.model("EnterRoom", {
        "user_id": fields.Integer(
            required = True,
            description = "ID do usuário"
        ),

        "room_id": fields.Integer(
            required = True,
            description = "ID da sala"
        ),

        "room_password": fields.String(
            required = False,
            description = "Senha da sala. Obrigatória apenas se a sala não for pública."
        )
    })