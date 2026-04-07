from utils.interfaces.command import Command
from user.service import UserService

class UserDetailsCommand(Command):
    """
    Comando para obter detalhes completos de um usuário.
    Retorna informações do perfil, incluindo problemas resolvidos,
    problemas criados, seguidores e status de follow.
    """
    def __init__(self, service: UserService, data):
        self.service = service
        self.data = data

    def execute(self):
        result = self.service.get_user(self.data)
        return result