from sqlalchemy import or_
from models.user.user import User


class AuthRepository:

    def get_by_login(self, session, login: str):

        return (
            session.query(User)
            .filter(
                or_(
                    User.email == login,
                    User.nickname == login
                )
            )
            .first()
        )