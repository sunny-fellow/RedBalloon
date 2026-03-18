from flask import request
import jwt

from utils.app_error import AppError

import os
from dotenv import load_dotenv

import os
from dotenv import load_dotenv
load_dotenv()
JWT_KEY = os.getenv("JWT_KEY")


def get_user_id():

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise AppError("Token não fornecido", 401)

    try:
        # formato: Bearer <token>
        token = auth_header.split(" ")[1]
    except IndexError:
        raise AppError("Formato de token inválido", 401)

    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=["HS256"])

        user_id = payload.get("user_id")

        if not user_id:
            raise AppError("Token inválido", 401)

        return user_id

    except jwt.ExpiredSignatureError:
        raise AppError("Token expirado", 401)

    except jwt.InvalidTokenError:
        raise AppError("Token inválido", 401)