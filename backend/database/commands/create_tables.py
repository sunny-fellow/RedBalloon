from utils.command import Command
from database.service import DatabaseService

class CreateTablesCommand(Command):
    def __init__(self, service: DatabaseService, password: str):
        self.service = service
        self.password = password

    def execute(self):
        self.service.create_tables(self.password)
        return {"message": "Tabelas criadas (ou já existiam)."}