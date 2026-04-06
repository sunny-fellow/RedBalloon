from utils.interfaces.command import Command
from database.service import DatabaseService

class FillTablesCommand:
    def __init__(self, service: DatabaseService, password: str):
        self.service = service
        self.password = password

    def execute(self):
        self.service.fill_tables(self.password)
        return {"message": "Tabelas preenchidas com dados de teste."}