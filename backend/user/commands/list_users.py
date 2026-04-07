from utils.interfaces.command import Command
from ..service import UserService

class ListUsersCommand(Command):
    """
    Comando para listar usuários com filtros opcionais.
    Permite buscar usuários por query textual e/ou país de origem.
    """
    def __init__(self, service: UserService, data):
        self.service = service
        self.data = data

    def execute(self):
        return self.service.list_users(self.data)