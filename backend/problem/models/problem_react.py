from flask_restx import fields

def ProblemReactModel(api):
    """
    Define o modelo de dados para reação a um problema. Este modelo é utilizado
    para validar requisições de like/dislike em problemas.
    """
    return api.model("ProblemReact", {
        "problem_id": fields.Integer(
            required = True,
            description = "ID do Problema"
        ),

        "user_id": fields.Integer(
            required = True,
            description = "ID do usuário que está submetendo sua avaliação"
        ),

        "react_type": fields.String(
            required = True,
            enum = ["LIKE", "DISLIKE"]
        )
    })