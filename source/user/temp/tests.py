from service import UserService
from user import UserDto as User

service = UserService()
user = User(None, "Fulano Di Town", "fulano.town@gmail.com", "fu_lano@@", "senha_do_fulano", False)

service.addUser(user)

service.listUsers()