from models.user.user import User
from models.user.user_follow import UserFollow
from models.submission.submission import Submission
from models.problem.problem import Problem
from models.enums import SubmissionStatus

from sqlalchemy import func, and_

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
            (Submission.status == SubmissionStatus.ACCEPTED)  # ajuste se for enum
        )

        if query:
            q = q.filter(User.name.ilike(f"%{query}%"))

        if country:
            q = q.filter(User.nationality == country)

        q = q.group_by(User.user_id).limit(50)

        return q.all()

    def get_user_full(self, session, user_id: int, requester_id: int):
        # -------- base user + stats --------
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
            User.user_id == user_id
        ).group_by(User.user_id).first()

        if not user_data:
            return None

        # -------- problemas resolvidos --------
        solved = session.query(
            Problem.problem_id,
            Problem.title,
            Problem.difficulty
        ).join(
            Submission,
            and_(
                Submission.problem_id == Problem.problem_id,
                Submission.user_id == user_id,
                Submission.status == "ACCEPTED"
            )
        ).group_by(Problem.problem_id).all()

        # -------- problemas criados --------
        created = session.query(
            Problem.problem_id,
            Problem.title,
            Problem.difficulty,
            func.count(func.distinct(Submission.user_id)).label("solved_count")
        ).outerjoin(
            Submission,
            and_(
                Submission.problem_id == Problem.problem_id,
                Submission.status == "ACCEPTED"
            )
        ).filter(
            Problem.creator_id == user_id
        ).group_by(Problem.problem_id).all()

        return user_data, solved, created

    def add(self, session, user: User):
        session.add(user)

    def delete(self, session, user: User):
        session.delete(user)

    def get_follow(self, session, follower_id: int, following_id: int):
        return session.query(UserFollow).filter(
            UserFollow.follower_id == follower_id,
            UserFollow.following_id == following_id
        ).first()

    def create_follow(self, session, follower_id: int, following_id: int):
        follow = UserFollow(
            follower_id=follower_id,
            following_id=following_id
        )
        session.add(follow)
        return follow

    def delete_follow(self, session, follow: UserFollow):
        session.delete(follow)