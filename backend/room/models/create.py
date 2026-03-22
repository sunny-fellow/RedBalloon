from flask_restx import fields


def CreateRoomModel(api):

    # -------- reutilizando partes do problem --------

    InputsOutputs = api.model("RoomProblemInputsOutputs", {
        "input": fields.String(required=True),
        "output": fields.String(required=True)
    })

    Checker = api.model("RoomProblemChecker", {
        "language": fields.String(
            required=True,
            enum=["PYTHON", "C", "CPP", "JAVA"]
        ),
        "source_code": fields.String(required=True)
    })

    # -------- problema NOVO (inline) --------

    NewProblem = api.model("RoomNewProblem", {
        "title": fields.String(required=True),
        "description": fields.String(required=True),

        "time_limit": fields.Integer(required=True),
        "memory_limit": fields.Integer(required=True),

        "validation_mode": fields.String(
            required=True,
            enum=["INPUTS_OUTPUTS", "CHECKER_ALGORITHM", "NO_VALIDATION"]
        ),

        "difficulty": fields.String(
            required=True,
            enum=["EASY", "MEDIUM", "HARD"]
        ),

        # validação
        "inputs_outputs": fields.List(fields.Nested(InputsOutputs)),
        "inputs": fields.List(fields.String),
        "checker": fields.Nested(Checker),
    })

    # -------- problema EXISTENTE --------

    ExistingProblem = api.model("RoomExistingProblem", {
        "problem_id": fields.Integer(
            required=True,
            description="ID de um problema já existente (público)"
        )
    })

    # -------- wrapper (define tipo + config sala) --------

    RoomProblemItem = api.model("RoomProblemItem", {

        # tipo
        "type": fields.String(
            required=True,
            enum=["EXISTING", "NEW"],
            description="Define se é problema existente ou novo"
        ),

        # config da sala
        "points": fields.Integer(
            required=True,
            description="Pontuação do problema na sala"
        ),

        "balloon_color": fields.String(
            required=True,
            description="Caminho/identificador da cor do balão"
        ),

        # payload (um dos dois)
        "existing_problem": fields.Nested(ExistingProblem),
        "new_problem": fields.Nested(NewProblem),
    })

    # -------- model principal --------

    return api.model("CreateRoom", {

        "user_id": fields.Integer(
            required=True,
            description="ID do usuário que está criando a sala"
        ),

        "room_name": fields.String(
            required=True,
            description="Nome da sala"
        ),

        "room_description": fields.String(
            required=False,
            description="Descrição da sala"
        ),

        "capacity": fields.Integer(
            required=True,
            description="Capacidade máxima de jogadores"
        ),

        "duration": fields.Integer(
            required=True,
            description="Duração da sala (minutos)"
        ),

        "room_password": fields.String(
            required=False,
            description="Senha da sala"
        ),

        # 🔥 aqui fica o principal
        "problems": fields.List(
            fields.Nested(RoomProblemItem),
            required=True,
            description="Lista de problemas da sala (novos ou existentes)"
        )
    })