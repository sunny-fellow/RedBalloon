# database/admin_service.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
from models import Base, engine
from utils.singleton import Singleton
from database.service import DatabaseService

load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
DATABASE_URL = os.getenv("DATABASE_URL")

@Singleton
class DatabaseAdminService:
    """
    Singleton responsável por operações administrativas do banco:
      - criar database
      - criar / reset / drop tabelas
      - preencher tabelas com dados de teste
    """
    
    def _check_password(self, password: str):
        if password != ADMIN_PASSWORD:
            raise PermissionError("Senha de administrador incorreta!")

    def create_database(self, password: str):
        self._check_password(password)
        from sqlalchemy.engine.url import make_url
        url = make_url(DATABASE_URL)
        db_name = url.database
        url = url.set(database="postgres")
        engine_tmp = create_engine(url, isolation_level="AUTOCOMMIT")
        with engine_tmp.connect() as conn:
            try:
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"Banco de dados '{db_name}' criado com sucesso!")
            except ProgrammingError:
                print(f"Banco de dados '{db_name}' já existe.")

    def create_tables(self, password: str):
        self._check_password(password)
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")

    def drop_tables(self, password: str):
        self._check_password(password)
        try:
            Base.metadata.drop_all(bind=engine)
            print("Todas as tabelas foram removidas com sucesso!")
        except Exception as e:
            print(f"Erro ao remover tabelas: {e}")
            raise

    def reset_tables(self, password: str):
        self._check_password(password)
        self.drop_tables(password)
        self.create_tables(password)

    def fill_tables(self, password: str):
        self._check_password(password)
        import os
        sql_file_path = os.path.join(os.path.dirname(__file__), "sql", "fill_tables.sql")
        if not os.path.exists(sql_file_path):
            raise FileNotFoundError(f"Arquivo SQL não encontrado: {sql_file_path}")
        with open(sql_file_path, "r", encoding="utf-8") as f:
            sql_commands = f.read()
        with engine.begin() as conn:
            conn.execute(text(sql_commands))
        print("Tabelas preenchidas com os dados do SQL com sucesso!")

    def undo_last_action(self, password: str):
        self._check_password(password)
        return {"obj": DatabaseService().undo_last()}