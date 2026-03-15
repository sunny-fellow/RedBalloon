from models.user.user import User

class UserRepository:

    def get_all(self, session):
        return session.query(User).all()

    def get_by_id(self, session, user_id: int):
        return session.query(User).filter(User.user_id == user_id).first()

    def add(self, session, user: User):
        session.add(user)

    def delete(self, session, user: User):
        session.delete(user)