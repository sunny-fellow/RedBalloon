from utils.interfaces.command import Command
from database.admin_service import DatabaseAdminService

class UndoActionCommand(Command):
    def __init__(self, service: DatabaseAdminService, password: str):
        self.service = service
        self.password = password

    def execute(self):
        return self.service.undo_last_action(self.password)