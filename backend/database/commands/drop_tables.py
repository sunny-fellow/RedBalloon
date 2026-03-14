from utils.command import Command
from database.service import DatabaseService

class DropTablesCommand(Command):
    def __init__(self, service: DatabaseService, password: str):
        self.service = service
        self.password = password

    def execute(self):
        self.service.drop_tables(self.password)
        return {"message": "Tabelas apagadas com sucesso."}