from .user import UserDto as User
import pandas as pd

class UserService():
    users_db = pd.DataFrame(columns=["id_user", "name", "email", "login", "password", "is_mod"])

    def listUsers(self):
        if len(self.users_db) > 0:
            print(self.users_db)
        else:
            print("No users")

    def addUser(self, user: User):
        self.users_db.loc[len(self.users_db)] = [len(self.users_db), user.name, user.email, user.login, user.password, user.is_mod]

    def removeUser(self, id_user: int):
        self.users_db = self.users_db[self.users_db["id_user"] != id_user]
        pass
