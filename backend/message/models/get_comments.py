from flask_restx import fields

def GetCommentsModel(api):
    return api.model("GetComments", {
        "context_type": fields.String(
            required=True,
            description="Tipo de Contexto da mensagem (Global | Problema | Solução)",
            enum=["GLOBAL", "PROBLEM", "SOLUTION"]
        ),

        "context_ref_id": fields.Integer(
            required=False,
            description="ID do problema ou da solução, caso esses sejam o context_type",
        ),

        "query": fields.String(
            required=False,
            description="Query de busca de comentários"
        ),

        "tags": fields.List(
            fields.String,
            required=False,
            description="Array de tags do comentário"
        ),

        "offset": fields.Integer(
            required = False,
            default = 0,
            description = "Offset de paginação das mensagens"
        )
    })