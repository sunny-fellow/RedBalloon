from flask_restx import Api

def create_api(app):
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Digite: Bearer <seu_token>"
        }
    }

    return Api(
        app,
        version="1.0",
        title="API RedBalloon",
        description="Documentação das rotas da aplicação Red Balloon",
        authorizations=authorizations,
        security='Bearer',
        doc=False
    )