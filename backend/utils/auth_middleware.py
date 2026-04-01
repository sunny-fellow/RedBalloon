import jwt
from flask import request, jsonify, g
from config import Config

def check_jwt_header():
    # Whitelist de rotas que não exigem token
    whitelist = ['auth', 'hello', 'static', 'restx_doc', 'database']
    
    if request.path.startswith(('/apidocs', '/swagger')):
        return

    if request.endpoint:
        endpoint_root = request.path.split('/')[1]
        print(endpoint_root)
        
        if endpoint_root in whitelist:
            return

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"status": "error", "message": "Token ausente"}), 401

    try:
        token = auth_header.split(" ")[1] if " " in auth_header else auth_header
        payload = jwt.decode(token, Config.JWT_KEY, algorithms=["HS256"])
        g.user = payload  # Disponível em todos os controllers
    
    except jwt.ExpiredSignatureError:
        return jsonify({"status": "error", "message": "Token expirado"}), 401
    
    except jwt.InvalidTokenError:
        return jsonify({"status": "error", "message": "Token inválido"}), 401