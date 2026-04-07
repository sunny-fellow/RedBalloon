from utils.interfaces.command import Command
from ..service import UserService

class UpdateUserCommand(Command):
    """
    Comando para atualizar dados de um usuário.
    Permite modificar campos como nome, nickname, email,
    senha, avatar, descrição e nacionalidade.
    """
    def __init__(self, service: UserService, user_id, data):
        self.service = service
        self.user_id = user_id
        self.data = data

    def execute(self):
        return self.service.update_user(self.user_id, self.data)