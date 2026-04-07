from utils.interfaces.command import Command
from ..service import UserService

class DeleteUserCommand(Command):
    """
    Comando para deletar (soft delete) um usuário do sistema.
    Realiza uma exclusão lógica, mantendo os dados no banco
    mas marcando o usuário como inativo.
    """
    def __init__(self, service: UserService, user_id):
        self.service = service
        self.user_id = user_id

    def execute(self):
        return self.service.delete_user(self.user_id)