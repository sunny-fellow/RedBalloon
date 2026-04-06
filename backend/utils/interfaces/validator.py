from abc import ABC, abstractmethod

class Validator(ABC):
    @staticmethod
    @abstractmethod
    def validate(data):
        """
        Deve lança uma exceção se ocorrer um erro
        """
        pass