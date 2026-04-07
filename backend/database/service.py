import os

from sqlalchemy import event, inspect
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoInspectionAvailable
from dotenv import load_dotenv
from models import SessionLocal
from utils.singleton import Singleton
from database.memento_manager import MementoManager
from models.memento.memento import Memento

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

@Singleton
class DatabaseService:
    """
    Singleton que fornece:
      - Execução de funções com session (run)
      - Undo do último memento global
      - clear_history
    """
    def __init__(self):
        self._memento = MementoManager()
        self.register_memento_listener(self._memento)

    @staticmethod
    def snapshot(obj):
        state = inspect(obj)
        data = {}

        for attr in state.mapper.column_attrs:
            key = attr.key
            hist = state.attrs[key].history

            if hist.deleted:
                value = hist.deleted[0]
            
            else:
                value = getattr(obj, key)

            data[key] = value

        return data

    def register_memento_listener(self, memento_manager):
        @event.listens_for(Session, "before_flush")
        def before_flush(session, flush_context, instances):
            user_id = session.info.get("user_id", None)

            # Objetos modificados
            for obj in session.dirty:
                if session.is_modified(obj, include_collections=False):
                    memento_manager.save(session, obj, self.snapshot(obj), "update", user_id)

            # Objetos deletados
            for obj in session.deleted:
                if isinstance(obj, Memento):
                    continue
                
                memento_manager.save(session, obj, self.snapshot(obj), "delete", user_id)

        @event.listens_for(Session, "after_flush")
        def after_flush(session, flush_context):
            user_id = session.info.get("user_id", None)

            # Só grava mementos de objetos novos depois do flush,
            # Garantindo que tenham PK
            for obj in session.new:
                if isinstance(obj, Memento):
                    continue
                
                memento_manager.save(session, obj, self.snapshot(obj), "create", user_id)

    def run(self, func, user_id: int = None):
        """
        Executa func(session) com session do SQLAlchemy.
        """
        with SessionLocal.begin() as session:
            session.info["user_id"] = user_id
            return func(session)

    def undo_last(self):
        """
        Reverte a última operação baseada em memento.
        """
        session: Session = SessionLocal()
        try:
            return self._to_dict(self._memento.undo_last(session))
        
        finally:
            session.close()

    def clear_history(self):
        """
        Limpa todos os mementos salvos.
        """
        self._memento.clear_history()
    
    @staticmethod
    def _to_dict(obj):
        """
        Converte um objeto SQLAlchemy em dicionário pronto para JSON.
        """
        try:
            state = inspect(obj)
        
        except NoInspectionAvailable:
            return obj

        data = {}
        for attr in state.mapper.column_attrs:
            key = attr.key
            data[key] = getattr(obj, key)

        return data