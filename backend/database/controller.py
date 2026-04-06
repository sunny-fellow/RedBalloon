from flask_restx import Namespace, Resource
from utils.handle_exceptions import handle_exceptions

from database.admin_service import DatabaseAdminService

from database.models.password import getPasswordModel

from database.commands.create_database import CreateDatabaseCommand
from database.commands.create_tables   import CreateTablesCommand
from database.commands.fill_tables     import FillTablesCommand
from database.commands.reset_tables    import ResetTablesCommand
from database.commands.drop_tables     import DropTablesCommand
from database.commands.undo_action     import UndoActionCommand

db_admin_service = DatabaseAdminService()
api = Namespace("database", description="Administração do Banco de Dados")

@api.route("/create_database")
class CreateDatabase(Resource):
    @handle_exceptions
    @api.expect(getPasswordModel(api), validate=True)
    def post(self):
        data = api.payload
        command = CreateDatabaseCommand(db_admin_service, data["password"])
        return command.execute(), 200

@api.route("/create_tables")
class CreateTables(Resource):
    @handle_exceptions
    @api.expect(getPasswordModel(api), validate=True)
    def post(self):
        data = api.payload
        command = CreateTablesCommand(db_admin_service, data["password"])
        return command.execute(), 200

@api.route("/reset_tables")
class ResetTables(Resource):
    @handle_exceptions
    @api.expect(getPasswordModel(api), validate=True)
    def post(self):
        data = api.payload
        command = ResetTablesCommand(db_admin_service, data["password"])
        return command.execute(), 200
        
@api.route("/drop_tables")
class DropTables(Resource):
    @handle_exceptions
    @api.expect(getPasswordModel(api), validate=True)
    def post(self):
        data = api.payload
        command = DropTablesCommand(db_admin_service, data["password"])
        return command.execute(), 200

@api.route("/fill_tables")
class FillTables(Resource):
    @handle_exceptions
    @api.expect(getPasswordModel(api), validate=True)
    def post(self):
        data = api.payload
        command = FillTablesCommand(db_admin_service, data["password"])
        return command.execute(), 200
        
@api.route("/undo_action")
class UndoActionByMemento(Resource):
    @handle_exceptions
    @api.expect(getPasswordModel(api), validate=True)
    def post(self):
        data = api.payload
        command = UndoActionCommand(db_admin_service, data["password"])
        return command.execute(), 200