from flask_restx import fields

def SubmissionModel(api):
    return api.model("SubmissionModel", {
        "user_id": fields.Integer(
            required = True,
            description = "ID do usuário que está fazendo a submissão"
        ),

        "problem_id": fields.Integer(
            required = True,
            description = "ID do problema ao qual a submissão está sendo feita"
        ),

        "language": fields.String(
            required = True,
            description = "linguagem de programação na qual o código do usuário foi escrito",
            enum = ["C", "CPP", "JAVA", "PYTHON"]
        ),

        "source_code": fields.String(
            required = True,
            description = "código desenvolvido pelo usuário"
        )
    })