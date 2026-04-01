import os
import sys

TEMPLATES = {
    "controller.py": """from flask_restx import Namespace, Resource
from utils.handle_exceptions import handle_exceptions
from {name}.service import {Name}Service

service = {Name}Service()

api = Namespace("{name}", description="")

# Models


# Commands


""",

    "service.py": """from database.service import DatabaseService
from utils.singleton import Singleton
from utils.app_error import AppError
from {name}.repository import {Name}Repository

@Singleton
class {Name}Service:

    def __init__(self):
        self.db_service = DatabaseService()
        self.repository = {Name}Repository()
""",

    "repository.py": """class {Name}Repository:

    def get_all(self, session):
        pass

    def get_by_id(self, session, id):
        pass

    def create(self, session, entity):
        session.add(entity)

    def delete(self, session, entity):
        session.delete(entity)
"""
}

def create_module(name):
    base_path = f"{name}"

    os.makedirs(base_path, exist_ok=True)

    # Cria arquivos principais
    for file, template in TEMPLATES.items():
        content = template.format(
            name=name,
            Name=name.capitalize()
        )

        with open(os.path.join(base_path, file), "w") as f:
            f.write(content)

    # Cria subpastas
    subfolders = ["models", "commands", "validators"]

    for folder in subfolders:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)

    print(f"Módulo '{name}' criado com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: python create_module.py nome_do_modulo")
    
    else:
        create_module(sys.argv[1])