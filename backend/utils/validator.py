from abc import ABC, abstractmethod

class Validator(ABC):
    @staticmethod
    @abstractmethod
    def validate(data):
        """
            Must raise an exception if an error occurred
        """
        pass