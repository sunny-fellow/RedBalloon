from flask_restx import fields

def CreateProblemModel(api):
    # Inputs + outputs
    InputsOutputs = api.model("ProblemInputsOutputs", {
        "input": fields.String(
            required=True,
            description="Entrada do caso de teste",
            example="2 3"
        ),
        "output": fields.String(
            required=True,
            description="Saída esperada",
            example="25"
        )
    })

    # Checker
    Checker = api.model("ProblemChecker", {
        "language": fields.String(
            required=True,
            enum=["PYTHON", "C", "CPP", "JAVA"],
            description="Linguagem do algoritmo checker"
        ),
        "source_code": fields.String(
            required=True,
            description="Código do algoritmo checker"
        )
    })

    # Model principal
    return api.model("ProblemCreate", {

        "creator_id": fields.Integer(
            required=True,
            description="ID de Usuário do Criador do Problema",
            example=3
        ),

        "title": fields.String(
            required=True,
            example="Soma dos Quadrados",
            description="Título do Problema"
        ),

        "description": fields.String(
            required=True,
            example="Informe o resultado de (a+b)² para a e b dados",
            description="Descrição do Problema (em .md)"
        ),

        "time_limit": fields.Integer(
            required=True,
            example=1000,
            description="Tempo limite de uma submissão (ms)"
        ),

        "memory_limit": fields.Integer(
            required=True,
            example=500,
            description="Memória limite de uma submissão (MB)"
        ),

        "validation_mode": fields.String(
            required=True,
            enum=[
                "INPUTS_OUTPUTS",
                "CHECKER_ALGORITHM",
                "NO_VALIDATION"
            ],
            description="Modo de validação da resposta"
        ),

        "difficulty": fields.String(
            required=True,
            enum=["EASY", "MEDIUM", "HARD"],
            description="Dificuldade do Problema"
        ),

        "private": fields.Boolean(
            required=False,
            default=False,
            description="Se pertence exclusivamente a uma sala"
        ),

        # INPUTS_OUTPUTS
        "inputs_outputs": fields.List(
            fields.Nested(InputsOutputs),
            required=False,
            description="Lista de casos de teste com entrada e saída"
        ),

        # NO_VALIDATION / CHECKER
        "inputs": fields.List(
            fields.String,
            required=False,
            description="Lista de entradas possíveis",
            default=None,
            example=None,
            nullable=True
        ),

        # CHECKER_ALGORITHM
        "checker": fields.Nested(
            Checker,
            required=False,
            description="Algoritmo usado para validar a saída",
            default=None,
            example=None,
            nullable=True
        )
    })