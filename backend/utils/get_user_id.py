# utils/get_user_id.py
import os
from dotenv import load_dotenv
from flask import request
import jwt
from utils.app_error import AppError

# Carrega variáveis de ambiente
load_dotenv()
JWT_KEY = os.getenv("JWT_KEY")

def get_user_id():
    """
    Retorna o user_id extraído do JWT enviado no header Authorization.
    Exceções são lançadas via AppError se o token estiver ausente, inválido ou expirado.
    """

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise AppError("Token não fornecido", 401)

    # Espera formato "Bearer <token>"
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise AppError("Formato de token inválido", 401)

    token = parts[1]

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