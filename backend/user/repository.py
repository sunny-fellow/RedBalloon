from models.user.user import User
from models.user.user_follow import UserFollow
from models.submission.submission import Submission
from models.problem.problem import Problem
from models.enums import SubmissionStatus
from sqlalchemy import func, and_
from datetime import datetime, timezone

class UserRepository:
    def get_all(self, session, query=None, country=None):
        q = session.query(
            User.user_id,
            User.name,
            User.avatar,
            User.nationality,
            func.count(func.distinct(UserFollow.follower_id)).label("followers_count"),
            func.count(func.distinct(Submission.problem_id)).label("solved_count")
        ).outerjoin(
            UserFollow, UserFollow.following_id == User.user_id
        ).outerjoin(
            Submission,
            (Submission.user_id == User.user_id) &
            (Submission.status == SubmissionStatus.ACCEPTED)
        ).filter(
            User.deleted_at.is_(None)  # NOVO: Filtrar apenas usuários ativos
        )
        
        if query:
            q = q.filter(User.name.ilike(f"%{query}%"))

        if country:
            q = q.filter(User.nationality == country)

        q = q.group_by(User.user_id).limit(50)

        return q.all()

    def get_user_full(self, session, user_id: int, requester_id: int):
        user_data = session.query(
            User.user_id,
            User.name,
            User.avatar,
            User.nationality,
            User.description,
            func.count(func.distinct(UserFollow.follower_id)).label("followers_count"),
            func.count(func.distinct(Submission.problem_id)).label("solved_count"),
            func.count(func.distinct(UserFollow.follower_id))
                .filter(UserFollow.follower_id == requester_id)
                .label("is_following")
        ).outerjoin(
            UserFollow, UserFollow.following_id == User.user_id
        ).outerjoin(
            Submission,
            and_(
                Submission.user_id == User.user_id,
                Submission.status == SubmissionStatus.ACCEPTED
            )
        ).filter(
            User.user_id == user_id,
            User.deleted_at.is_(None)  # NOVO: Filtrar apenas usuários ativos
        ).group_by(User.user_id).first()

        if not user_data:
            return None

        # Problemas resolvidos (mantém o filtro por usuário ativo nos relacionamentos)
        solved = session.query(
            Problem.problem_id,
            Problem.title,
            Problem.difficulty
        ).join(
            Submission,
            and_(
                Submission.problem_id == Problem.problem_id,
                Submission.user_id == user_id,
                Submission.status == SubmissionStatus.ACCEPTED
            )
        ).filter(
            Problem.deleted_at.is_(None) if hasattr(Problem, 'deleted_at') else True  # Se Problem também tiver soft delete
        ).group_by(Problem.problem_id).all()

        # Problemas criados
        created = session.query(
            Problem.problem_id,
            Problem.title,
            Problem.difficulty,
            func.count(func.distinct(Submission.user_id)).label("solved_count")
        ).outerjoin(
            Submission,
            and_(
                Submission.problem_id == Problem.problem_id,
                Submission.status == SubmissionStatus.ACCEPTED
            )
        ).filter(
            Problem.creator_id == user_id,
            Problem.deleted_at.is_(None) if hasattr(Problem, 'deleted_at') else True
        ).group_by(Problem.problem_id).all()

        return user_data, solved, created

    def add(self, session, user: User):
        session.add(user)

    # MODIFICADO: Substituir delete físico por soft delete
    def soft_delete(self, session, user_id: int):
        """Soft delete - marca o usuário como deletado"""
        user = session.query(User).filter(
            User.user_id == user_id,
            User.deleted_at.is_(None)  # Apenas usuários não deletados
        ).first()
        
        if user:
            user.deleted_at = datetime.now(timezone.utc)
            return True
        return False

    # NOVO: Método para restaurar usuário
    def restore(self, session, user_id: int):
        """Restaura um usuário deletado"""
        user = session.query(User).filter(
            User.user_id == user_id,
            User.deleted_at.isnot(None)  # Apenas usuários deletados
        ).first()
        
        if user:
            user.deleted_at = None
            return True
        return False

    # NOVO: Método para exclusão física (se necessário)
    def permanent_delete(self, session, user_id: int):
        """Exclusão física permanente (usar com cautela)"""
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            return True
        return False

    # MODIFICADO: Incluir filtro de deleted_at
    def get_follow(self, session, follower_id: int, following_id: int):
        return session.query(UserFollow).filter(
            UserFollow.follower_id == follower_id,
            UserFollow.following_id == following_id
        ).join(
            User, User.user_id == UserFollow.following_id
        ).filter(
            User.deleted_at.is_(None)  # Não pode seguir usuário deletado
        ).first()

    def create_follow(self, session, follower_id: int, following_id: int):
        # Verificar se o usuário a ser seguido existe e não está deletado
        user = session.query(User).filter(
            User.user_id == following_id,
            User.deleted_at.is_(None)
        ).first()
        
        if not user:
            raise AppError("Usuário não encontrado ou está inativo", 404)
            
        follow = UserFollow(
            follower_id=follower_id,
            following_id=following_id
        )
        session.add(follow)
        return follow

    def delete_follow(self, session, follow: UserFollow):
        session.delete(follow)

    # MODIFICADO: Contar apenas usuários ativos
    def count_users(self, session):
        return session.query(func.count(User.user_id)).filter(
            User.deleted_at.is_(None)
        ).scalar()

    # MODIFICADO: Buscar apenas usuários ativos
    def get_by_id(self, session, user_id: int):
        return session.query(User).filter(
            User.user_id == user_id,
            User.deleted_at.is_(None)
        ).first()

    # MODIFICADO: Verificar existência apenas de usuários ativos
    def user_exists(self, session, user_id: int) -> bool:
        return session.query(User.user_id).filter(
            User.user_id == user_id,
            User.deleted_at.is_(None)
        ).first() is not None
    
    # NOVO: Buscar usuário incluindo deletados (para admin/restauração)
    def get_by_id_including_deleted(self, session, user_id: int):
        return session.query(User).filter(User.user_id == user_id).first()