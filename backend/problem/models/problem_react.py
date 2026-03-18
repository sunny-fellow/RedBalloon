from flask_restx import fields

def ProblemReactModel(api):
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