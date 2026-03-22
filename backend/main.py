from flask import Flask
from flask_socketio import SocketIO
from flask_swagger_ui import get_swaggerui_blueprint

# Configurações e Middlewares
from config import Config
from auth_middleware import check_jwt_header
from api_factory import create_api

# Importa controllers
from auth.controller        import api as auth_ns
from database.controller    import api as database_ns
from message.controller     import api as message_ns
from problem.controller     import api as problem_ns
from room.controller        import api as room_ns
from submission.controller  import api as submission_ns
from user.controller        import api as user_ns


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.api = create_api(self.app)
        
        self._setup_middlewares()
        self._register_namespaces()
        self._configure_swagger_ui()

    def _setup_middlewares(self):
        @self.app.route("/")
        def hello():
            return {"message": "RedBalloon API Online"}, 200

        # Aplica a validação JWT globalmente
        self.app.before_request(check_jwt_header)

    def _register_namespaces(self):
        self.api.add_namespace(auth_ns, path="/auth")
        self.api.add_namespace(problem_ns, path="/problem")
        self.api.add_namespace(message_ns, path="/message")
        self.api.add_namespace(room_ns, path="/room")
        self.api.add_namespace(submission_ns, path="/submission")
        self.api.add_namespace(user_ns, path="/user")
        self.api.add_namespace(database_ns, path="/database")

    def _configure_swagger_ui(self):
        swagger_bp = get_swaggerui_blueprint(
            "/apidocs", "/swagger.json", 
            config={"app_name": "RedBalloon API"}
        )
        self.app.register_blueprint(swagger_bp, url_prefix="/apidocs")

    def run(self):
        self.socketio.run(
            self.app, 
            host="0.0.0.0", 
            port=Config.PORT, 
            debug=Config.DEBUG
        )

if __name__ == "__main__":
    server = Server()
    server.run()