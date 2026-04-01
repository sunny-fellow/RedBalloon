# utils/get_user_id.py
import os
from dotenv import load_dotenv
from flask import request
import jwt
from utils.app_error import AppError

load_dotenv()

JWT_KEY = os.getenv("JWT_KEY")

if not JWT_KEY:
    JWT_KEY = "dev-secret-key"

def get_user_id():

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise AppError("Token não fornecido", 401)

    parts = auth_header.split()

    if len(parts) == 1:
        token = parts[0]
    
    elif len(parts) == 2 and parts[0].lower() == "bearer":
        token = parts[1]
    
    else:
        raise AppError("Formato de token inválido", 401)

    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=["HS256"])

        user_id = payload.get("user_id") or payload.get("sub")

        if user_id is None:
            raise AppError("Token inválido", 401)

        return int(user_id)

    except jwt.ExpiredSignatureError:
        raise AppError("Token expirado", 401)

    except jwt.InvalidTokenError:
        raise AppError("Token inválido", 401)