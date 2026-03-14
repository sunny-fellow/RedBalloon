from utils.command import Command
from database.admin_service import DatabaseAdminService

class CreateDatabaseCommand(Command):
    def __init__(self, service: DatabaseAdminService, password: str):
        self.service = service
        self.password = password

    def execute(self):
        self.service.create_database(self.password)
        return {"message": "Banco de dados criado (ou já existia)."}