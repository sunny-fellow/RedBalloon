from execution.executors.docker_executor import DockerExecutor
from utils.interfaces.code_executor import Executor

class CExecutor(DockerExecutor, Executor):
    """
    Executor específico para C
    """
    def __init__(self):
        super().__init__("sandbox-c")
    
    def get_language(self) -> str:
        return "C"

    def execute(self, source_code, input_data, time_limit, memory_limit):
        return super().execute(source_code, input_data, time_limit, memory_limit, "c")