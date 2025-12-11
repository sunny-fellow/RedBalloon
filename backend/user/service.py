import pandas as pd

# OBS.: Para a primeira entrega, os dados serão armazenados em memória usando um DataFrame do Pandas.
# Em entregas futuras, a implementação será alterada para utilizar um banco de dados real.

class UserService:
    def __init__(self):
        self.users_db = pd.DataFrame(columns=["id_user", "name", "email", "login", "password", "is_mod"])
        self.last_id = 0

    def list_users(self):
        return self.users_db.to_dict(orient='records')

    def create_user(self, data):
        # gera novo ID
        self.last_id += 1

        new_user = {
            "id_user": self.last_id,
            "name": data.get("name"),
            "email": data.get("email"),
            "login": data.get("login"),
            "password": data.get("password"),
            "is_mod": data.get("is_mod", False)
        }

        # adiciona ao DataFrame
        self.users_db.loc[len(self.users_db)] = new_user

        return new_user

    def delete_user(self, id_user):
        # verifica se existe
        if id_user not in self.users_db["id_user"].values:
            return False

        # remove e reorganiza o índice
        self.users_db = self.users_db[self.users_db["id_user"] != id_user].reset_index(drop=True)
        return True
    
    def update_user(self, id_user, data):
        # verifica se existe
        if id_user not in self.users_db["id_user"].values:
            return False

        # obtém o índice do usuário
        idx = self.users_db.index[self.users_db["id_user"] == id_user][0]

        # atualiza os campos passados em data
        for key in ["name", "email", "login", "password", "is_mod"]:
            if key in data:
                self.users_db.at[idx, key] = data[key]

        return self.users_db.loc[idx].to_dict()