import functools
from werkzeug.exceptions import HTTPException
from utils.validation_error import ValidationError
import traceback

def handle_exceptions(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except ValidationError as e:
            return {"message": str(e)}, 400

        except IOError as e:
            return {"message": f"Erro de armazenamento: {str(e)}"}, 500

        except HTTPException as e:
            return {"message": e.description}, e.code

        except Exception as e:
            traceback.print_exc()
            return {"message": f"Erro interno inesperado: {str(e)}"}, 500

    return wrapper