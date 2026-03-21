from abc import ABC, abstractmethod

class Executor(ABC):
    @abstractmethod
    def execute(self, source_code: str, input_data: str, time_limit: int):
        pass