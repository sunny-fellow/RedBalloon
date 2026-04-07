# execution/executors/python_executor.py
from execution.executors.docker_executor import DockerExecutor
from utils.interfaces.code_executor import Executor

class PythonExecutor(DockerExecutor, Executor):
    def __init__(self):
        super().__init__("sandbox-python")
    
    def get_language(self) -> str:
        return "PYTHON"

    def execute(self, source_code, input_data, time_limit, memory_limit):
        return super().execute(source_code, input_data, time_limit, memory_limit, "python")