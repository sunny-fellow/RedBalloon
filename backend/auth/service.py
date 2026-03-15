import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

from database.service import DatabaseService
from utils.singleton import Singleton
from utils.validation_error import ValidationError
from auth.repository import AuthRepository
from models.user.user import User

import os
from dotenv import load_dotenv
load_dotenv()
JWT_KEY = os.getenv("JWT_KEY")
TOKEN_EXPIRATION_HOURS = int(os.getenv("TOKEN_EXPIRATION_HOURS"))

from auth.validators.login import LoginValidator
from auth.validators.register import RegisterValidator

@Singleton
class AuthService:

    def __init__(self):
        self.db_service = DatabaseService()
        self.repository = AuthRepository()

    def login(self, data: dict):

        LoginValidator().validate(data)

        login = data["login"]
        password = data["password"]

        def func(session):

            user = self.repository.get_by_login(session, login)

            if not user:
                raise ValidationError("Credenciais inválidas.")

            if not bcrypt.checkpw(
                password.encode("utf-8"),
                user.password.encode("utf-8")
            ):
                raise ValidationError("Credenciais inválidas.")

            payload = {
                "user_id": user.user_id,
                "nickname": user.nickname,
                "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRATION_HOURS)
            }

            token = jwt.encode(payload, JWT_KEY, algorithm="HS256")

            return {
                "token": token,
                "user": {
                    "user_id": user.user_id,
                    "nickname": user.nickname,
                    "email": user.email
                }
            }

        return self.db_service.run(func)
    
    def register(self, data: dict):

        RegisterValidator().validate(data)

        nickname = data.get("nickname")
        email = data.get("email")
        password = data.get("password")

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        new_user = User(
            name=data.get("name"),
            nickname=nickname,
            email=email,
            password=hashed_password,
            avatar=data.get("avatar"),
            nationality=data.get("nationality"),
            description= "Hello, I'm " + data.get("name") + "!",
            created_at=datetime.now(timezone.utc).isoformat()
        )

        def func(session):

            existing_user = self.repository.get_by_login(session, nickname)
            existing_email = self.repository.get_by_login(session, email)

            if existing_user or existing_email:
                raise ValidationError("Nickname ou E-mail já está em uso.")

            email_user = session.query(User).filter(User.email == email).first()

            if email_user:
                raise ValidationError("Email já está em uso.")

            session.add(new_user)
            session.flush()

            return {
                "user_id": new_user.user_id,
                "nickname": new_user.nickname,
                "email": new_user.email
            }

        return self.db_service.run(func)