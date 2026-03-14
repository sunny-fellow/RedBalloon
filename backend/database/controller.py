from flask_restx import Namespace, Resource

# Import do Service
from database.admin_service import DatabaseAdminService
db_admin_service = DatabaseAdminService()

# Import dos Models
from database.models.password import getPasswordModel

# Import dos ConcreteCommands
from database.commands.create_database import CreateDatabaseCommand
from database.commands.create_tables   import CreateTablesCommand
from database.commands.fill_tables     import FillTablesCommand
from database.commands.reset_tables    import ResetTablesCommand
from database.commands.drop_tables     import DropTablesCommand
from database.commands.undo_action     import UndoActionCommand

# Definição do Namespace
api = Namespace("database", description="Administração do Banco de Dados")


# ----------------- API Endpoints -----------------

@api.route("/create_database")
class CreateDatabase(Resource):
    @api.expect(getPasswordModel(api))
    def post(self):
        data = api.payload
        try:
            command = CreateDatabaseCommand(db_admin_service, data["password"])
            return command.execute(), 200
        except Exception as e:
            return {"message": str(e)}, 400


@api.route("/create_tables")
class CreateTables(Resource):
    @api.expect(getPasswordModel(api))
    def post(self):
        data = api.payload
        try:
            command = CreateTablesCommand(db_admin_service, data["password"])
            return command.execute(), 200
        except Exception as e:
            return {"message": str(e)}, 400


@api.route("/reset_tables")
class ResetTables(Resource):
    @api.expect(getPasswordModel(api))
    def post(self):
        data = api.payload
        try:
            command = ResetTablesCommand(db_admin_service, data["password"])
            return command.execute(), 200
        except Exception as e:
            return {"message": str(e)}, 400
        
@api.route("/drop_tables")
class DropTables(Resource):
    @api.expect(getPasswordModel(api))
    def post(self):
        data = api.payload
        try:
            command = DropTablesCommand(db_admin_service, data["password"])
            return command.execute(), 200
        except Exception as e:
            return {"message": str(e)}, 400


@api.route("/fill_tables")
class FillTables(Resource):
    @api.expect(getPasswordModel(api))
    def post(self):
        data = api.payload
        try:
            command = FillTablesCommand(db_admin_service, data["password"])
            return command.execute(), 200
        except Exception as e:
            return {"message": str(e)}, 400
        
@api.route("/undo_action")
class UndoActionByMemento(Resource):
    @api.expect(getPasswordModel(api))
    def post(self):
        data = api.payload
        try: 
            command = UndoActionCommand(db_admin_service, data["password"])
            return command.execute(), 200
        except Exception as e:
            return {"message": str(e)}, 400