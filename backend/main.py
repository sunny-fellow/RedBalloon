# backend/main.py
from flask import Flask
from flask_restx import Api
from flask_swagger_ui import get_swaggerui_blueprint

# Importa namespaces (controllers)
from user.controller import api as user_controller
from database.controller import api as database_controller
from auth.controller import api as auth_controller
from problem.controller import api as problem_controller

# The "Server" class is a facade class.
class Server:

    def __init__(self):
        self.app = Flask(__name__)
        self.api = None

    def configure_routes(self):
        @self.app.route("/")
        def hello():
            return {
                "message": "Hello World!",
                "warn": "if you're looking for the documentation, check /apidocs"
            }, 200

    def configure_api(self):
        self.api = Api(
            self.app,
            version="1.0",
            title="API RedBalloon",
            description="Documentação das rotas da aplicação Red Balloon",
            doc=False,
        )

    def register_controllers(self):
        self.api.add_namespace(auth_controller, path="/auth")
        self.api.add_namespace(user_controller, path="/user")
        self.api.add_namespace(problem_controller, path="/problem")
        self.api.add_namespace(database_controller, path="/database")

    def configure_swagger(self):
        swaggerui_blueprint = get_swaggerui_blueprint(
            "/apidocs",
            "/swagger.json",
            config={"app_name": "RedBalloon API"}
        )

        self.app.register_blueprint(swaggerui_blueprint, url_prefix="/apidocs")

    def build(self):
        self.configure_routes()
        self.configure_api()
        self.register_controllers()
        self.configure_swagger()

    def run(self):
        self.build()
        self.app.run(debug=True)

if __name__ == "__main__":
    Server().run()
