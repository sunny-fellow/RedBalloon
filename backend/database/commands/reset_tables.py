from utils.interfaces.command import Command
from database.service import DatabaseService

class ResetTablesCommand:
    def __init__(self, service: DatabaseService, password: str):
        self.service = service
        self.password = password

    def execute(self):
        self.service.reset_tables(self.password)
        return {"message": "Tabelas resetadas com sucesso."}