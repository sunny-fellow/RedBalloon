from flask_restx import fields

def SubmissionReactModel(api):
    """
    Define o modelo de dados para reação a uma submissão.
    Este modelo é utilizado para validar requisições de like/dislike
    em submissões de código.
    """
    return api.model("SubmissionReact", {
        "user_id": fields.Integer(
            required = True,
            description = "ID do usuário que está submetendo reação"
        ),

        "submission_id": fields.Integer(
            required = True,
            description = "ID da submissão à qual está reagindo"
        ),

        "reaction": fields.String(
            required = True,
            description = "Reação do Usuário",
            enum = ["LIKE", "DISLIKE"]
        )
    })