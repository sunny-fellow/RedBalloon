from execution.executors.docker_executor import DockerExecutor
from execution.executors.code_executor import Executor

class PythonExecutor(DockerExecutor, Executor):
    def __init__(self):
        super().__init__("sandbox-python")

    def execute(self, source_code, input_data, time_limit, memory_limit):
        return super().execute(source_code, input_data, time_limit, memory_limit, "python")