from temp.service import UserService
from temp.user import UserDto as User
import os

service = UserService()

def readUser() -> User:

    name = str(input("Name: "))
    email = str(input("Email: "))
    login = str(input("Login: "))
    password = str(input("Password: "))
    is_mod = str(input("Is Moderator [y\\n]: ")) == "y"

    return User(None, name, email, login, password, is_mod)

while True:
    os.system("cls")
    print("=*= USER CRUD =*=\n")
    print("1. Add User")
    print("2. List Users")
    print("3. Delete User")
    print("0. Quit")
    opt = input("Choose one opt: ")
    
    match opt:
        case "1":
            os.system("cls")
            print("--- New User ---\n")
            service.addUser(readUser())
            print("retornou")
        case "2":
            os.system("cls")
            print("--- Users ---\n")
            service.listUsers()
            _ = input("\nAny key to continue:")
        case "3":
            os.system("cls")
            print("--- Delete User ---\n")
            id = int(input("Enter the user id to delete: "))
            service.removeUser(id)
        case _:
            os.system("cls")
            break