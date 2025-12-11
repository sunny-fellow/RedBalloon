from flask import Flask
from flask_restx import Api
from flask_swagger_ui import get_swaggerui_blueprint

# Importa namespaces (controllers)
from user.controller import api as user_controller

class Server:
    def __init__(self):
        self.app = Flask(__name__)

        # rota padrão, para testar se o servidor está ativo
        @self.app.route("/")
        def hello():
            return {"message": "Hello World"}, 200

        self.api = Api(
            self.app,
            version="1.0",
            title="API RedBalloon",
            description="Documentação das rotas da aplicação Red Balloon",
            doc=False,  # desativa o Swagger nativo
        )

        # Adiciona as rotas definidas nos controllers
        self.api.add_namespace(user_controller, path="/user")

        SWAGGER_URL = "/apidocs"
        API_URL = "/swagger.json"

        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={
                "app_name": "RedBalloon API"
            }
        )

        self.app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    Server().run()
