import pandas as pd
import json
import os
import re

class ValidationError(Exception):
    """Exceção personalizada para erros de validação."""
    pass

class UserService:
    def __init__(self, storage_file='users.json'):
        self.storage_file = storage_file
        self.users_db = pd.DataFrame(columns=["id_user", "name", "email", "login", "password", "is_mod"])
        self.last_id = 0
        self._load_from_file()  # Carrega dados do arquivo ao iniciar

    def _load_from_file(self):
        """Carrega os usuários do arquivo JSON para o DataFrame em memória."""
        if not os.path.exists(self.storage_file):
            return  # Arquivo não existe, começa vazio

        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data:
                self.users_db = pd.DataFrame(data)
                # Garante que as colunas estejam na ordem correta
                if not self.users_db.empty:
                    self.last_id = self.users_db['id_user'].max()
                else:
                    self.last_id = 0
            else:
                self.users_db = pd.DataFrame(columns=["id_user", "name", "email", "login", "password", "is_mod"])
                self.last_id = 0
        
        except (IOError, json.JSONDecodeError) as e:
            # Em caso de erro de leitura, começa vazio, mas loga o erro (aqui apenas print para simplicidade)
            print(f"Erro ao carregar arquivo {self.storage_file}: {e}. Iniciando com banco vazio.")
            self.users_db = pd.DataFrame(columns=["id_user", "name", "email", "login", "password", "is_mod"])
            self.last_id = 0

    def _save_to_file(self):
        """Salva o DataFrame atual no arquivo JSON."""
        try:
            self.users_db.to_json(self.storage_file, orient='records', indent=2, force_ascii=False)
        
        except IOError as e:
            print(f"Erro ao salvar arquivo {self.storage_file}: {e}")
            # Relança a exceção para que a camada superior (controller) possa tratá-la
            raise IOError(f"Não foi possível salvar os dados no arquivo: {e}")

    def _validate_login(self, login):
        """Valida as regras do login."""
        if not login or not login.strip():
            raise ValidationError("O campo 'login' não pode ser vazio.")
        
        if len(login) > 12:
            raise ValidationError("O 'login' deve ter no máximo 12 caracteres.")
        
        if re.search(r'\d', login):
            raise ValidationError("O 'login' não pode conter números.")

    def _validate_password(self, password):
        """
        Valida a senha seguindo a política padrão da AWS IAM:
        - Tamanho mínimo 8 e máximo 128 caracteres.
        - Pelo menos três dos quatro tipos: maiúscula, minúscula, número, caractere especial.
        """
        if not password:
            raise ValidationError("O campo 'password' não pode ser vazio.")
        
        if len(password) < 8 or len(password) > 128:
            raise ValidationError("A 'senha' deve ter entre 8 e 128 caracteres.")

        # Verifica a presença de tipos de caracteres
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        
        # Caracteres especiais comuns (baseado na lista da AWS)
        special_chars = r"[!@#$%^&*()_+\-=\[\]{}|']"
        has_special = bool(re.search(special_chars, password))

        types_count = sum([has_upper, has_lower, has_digit, has_special])
        if types_count < 3:
            raise ValidationError(
                "A 'senha' deve conter pelo menos três dos seguintes tipos: "
                "letras maiúsculas, letras minúsculas, números e caracteres especiais."
            )

    def list_users(self):
        """Lista todos os usuários."""
        return self.users_db.to_dict(orient='records')

    def create_user(self, data):
        """Cria um novo usuário com validações e salva no arquivo."""
        # --- Validações ---
        login = data.get("login")
        password = data.get("password")

        self._validate_login(login)
        self._validate_password(password)

        # Validação adicional: email único (opcional, mas boa prática)
        if login in self.users_db["login"].values:
            raise ValidationError(f"O login '{login}' já está em uso.")

        # --- Criação do usuário ---
        self.last_id += 1
        new_user = {
            "id_user": self.last_id,
            "name": data.get("name"),
            "email": data.get("email"),
            "login": login,
            "password": password,  # Em um cenário real, a senha deveria ser hasheada!
            "is_mod": data.get("is_mod", False)
        }

        # Adiciona ao DataFrame
        self.users_db.loc[len(self.users_db)] = new_user

        try:
            self._save_to_file()
        
        except IOError as e:
            # Se falhar ao salvar, reverte a operação em memória para consistência
            self.users_db = self.users_db[self.users_db["id_user"] != self.last_id].reset_index(drop=True)
            self.last_id -= 1
            raise IOError(f"Erro ao salvar novo usuário: {e}")
        
        return new_user

    def delete_user(self, id_user):
        """Deleta um usuário pelo ID e atualiza o arquivo."""
        if id_user not in self.users_db["id_user"].values:
            return False

        # Guarda o estado anterior para possível rollback
        users_backup = self.users_db.copy()

        # Remove e reorganiza o índice
        self.users_db = self.users_db[self.users_db["id_user"] != id_user].reset_index(drop=True)

        # --- Persistência ---
        try:
            self._save_to_file()
        
        except IOError as e:
            # Rollback em caso de erro no arquivo
            self.users_db = users_backup
            raise IOError(f"Erro ao deletar usuário: {e}")

        return True

    def update_user(self, id_user, data):
        """Atualiza um usuário com validações e salva no arquivo."""
        if id_user not in self.users_db["id_user"].values:
            return False

        # Guarda o estado anterior para possível rollback
        users_backup = self.users_db.copy()
        idx = self.users_db.index[self.users_db["id_user"] == id_user][0]

        try:
            if "login" in data and data["login"] is not None:
                new_login = data["login"]
                self._validate_login(new_login)
                # Verifica se o novo login já existe em outro usuário
                
                if new_login in self.users_db["login"].values and new_login != self.users_db.at[idx, "login"]:
                    raise ValidationError(f"O login '{new_login}' já está em uso.")
                
                self.users_db.at[idx, "login"] = new_login

            if "password" in data and data["password"] is not None:
                self._validate_password(data["password"])
                self.users_db.at[idx, "password"] = data["password"]

        except ValidationError as e:
            # Se houver erro de validação, não salva nada
            raise e

        # Atualiza os outros campos sem validação especial
        for key in ["name", "email", "is_mod"]:
            if key in data:
                self.users_db.at[idx, key] = data[key]

        # --- Persistência ---
        try:
            self._save_to_file()
        
        except IOError as e:
            # Rollback em caso de erro no arquivo
            self.users_db = users_backup
            raise IOError(f"Erro ao atualizar usuário: {e}")

        return self.users_db.loc[idx].to_dict()