import functools
import traceback

from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from utils.app_error import AppError

def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except AppError as e:
            return e.to_dict(), e.code

        except IntegrityError as e:
            traceback.print_exc()
            return {
                "message": "Erro de integridade no banco de dados.",
                "code": 400
            }, 400

        except IOError as e:
            return {
                "message": f"Erro de armazenamento: {str(e)}",
                "code": 500
            }, 500

        except HTTPException as e:
            return {
                "message": e.description,
                "code": e.code
            }, e.code

        except Exception as e:
            traceback.print_exc()
            return {
                "message": f"Erro interno inesperado: {str(e)}",
                "code": 500
            }, 500

    return wrapper