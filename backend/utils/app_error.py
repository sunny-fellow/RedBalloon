class AppError(Exception):
    def __init__(self, message: str, code: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code

    def to_dict(self):
        return {
            "message": self.message,
            "code": self.code
        }