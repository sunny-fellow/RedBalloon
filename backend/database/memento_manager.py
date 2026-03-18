from sqlalchemy.orm import Session
from sqlalchemy import inspect, desc
from models.memento.memento import Memento


class MementoManager:
    """
    Gerencia mementos persistidos no banco para permitir undo por usuário.
    """

    def save(self, session: Session, obj, snapshot: dict, action: str, user_id: int = None):
        """
        Salva um memento no banco.

        action:
            create -> objeto foi criado
            update -> objeto foi modificado
            delete -> objeto foi deletado
        """

        cls = obj.__class__
        pk = self._get_primary_key(obj)

        memento = Memento(
            user_id=user_id,
            entity_class=cls.__name__,
            entity_pk=str(pk),
            action=action,
            snapshot=snapshot
        )

        session.add(memento)

    def undo_last(self, session: Session, user_id: int = None):
        """
        Reverte a última operação salva no histórico do usuário.
        """
        memento = (
            session.query(Memento)
            .filter(Memento.user_id == user_id)
            .order_by(desc(Memento.created_at))
            .first()
        )

        if not memento:
            print("Nenhum histórico de alterações!")
            return None

        cls = self._resolve_class(memento.entity_class)
        snapshot = memento.snapshot
        action = memento.action

        obj = None
        if memento.entity_pk is not None:
            try:
                pk = self._parse_pk(memento.entity_pk)
                obj = session.get(cls, pk)
            except:
                obj = None

        # ---- undo create ----
        if action == "create":
            if obj:
                session.delete(obj)

        # ---- undo delete ----
        elif action == "delete":
            clean_snapshot = {k: v for k, v in snapshot.items() if not k.startswith("_sa_")}
            obj = cls(**clean_snapshot)
            session.add(obj)

        # ---- undo update ----
        elif action == "update":
            if obj:
                for field, value in snapshot.items():
                    if not field.startswith("_sa_"):
                        setattr(obj, field, value)

        # remove o memento depois de desfazer
        session.delete(memento)
        session.commit()

        if obj:
            session.refresh(obj)

        return obj

    def clear_history(self, session: Session, user_id: int = None):
        """
        Limpa histórico de mementos.
        """
        query = session.query(Memento)

        if user_id is not None:
            query = query.filter(Memento.user_id == user_id)

        query.delete()
        session.commit()

    def _get_primary_key(self, obj):
        """
        Obtém a chave primária do objeto SQLAlchemy.
        Suporta chaves compostas.
        """
        mapper = inspect(obj).mapper
        pk_values = tuple(getattr(obj, col.key) for col in mapper.primary_key)

        if len(pk_values) == 1:
            return pk_values[0]

        return pk_values

    def _parse_pk(self, pk_str):
        """
        Converte PK salva em string de volta para o formato original.
        """
        if pk_str.startswith("("):
            return tuple(map(int, pk_str.strip("()").split(",")))
        return int(pk_str)

    def _resolve_class(self, class_name: str):
        """
        Resolve string da classe para classe real do model.
        """
        from models import Base

        for mapper in Base.registry.mappers:
            cls = mapper.class_
            if cls.__name__ == class_name:
                return cls

        raise ValueError(f"Classe '{class_name}' não encontrada nos models.")