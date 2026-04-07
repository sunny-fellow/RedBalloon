from flask_restx import fields

def CommentModel(api):
    """
    Define o modelo de dados para criação de um comentário. Este modelo é utilizado para validar e
    documentar a estrutura esperada no payload de requisição para criar um novo comentário.
    """
    return api.model("CommentModel", {
        "user_id": fields.Integer(
            required = True,
            description = "ID do usuário que requisitou"
        ),

        "context_type": fields.String(
            required = True,
            description = "Tipo de Contexto da mensagem (Global | Problema | Solução)",
            enum=["GLOBAL", "PROBLEM", "SOLUTION"]
        ),

        "context_ref_id": fields.Integer(
            required = False,
            description = "ID do problema ou da solução, caso esses sejam o context_type",
        ),

        "parent_message": fields.Integer(
            required = False,
            description = "ID da mensagem pai da mensagem que está sendo mandada"
        ),

        "user_id": fields.Integer(
            required = True,
            description = "ID do usuário que está submetendo a mensagem"
        ),

        "message": fields.String(
            required = True,
            description = "Conteúdo da mensagem"
        ),

        "tags": fields.List(
            fields.String,
            required=False,
            description="Array de tags do comentário"
        )
    })