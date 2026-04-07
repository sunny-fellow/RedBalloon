from execution.executors.docker_executor import DockerExecutor
from utils.interfaces.code_executor import Executor

class CppExecutor(DockerExecutor, Executor):
    def __init__(self):
        super().__init__("sandbox-cpp")
    
    def get_language(self) -> str:
        return "CPP"

    def execute(self, source_code, input_data, time_limit, memory_limit):
        return super().execute(source_code, input_data, time_limit, memory_limit, "cpp")