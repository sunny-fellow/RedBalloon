from execution.executors import Executor, PythonExecutor, CExecutor, CppExecutor, JavaExecutor

class ExecutorFactory:
    @staticmethod
    def get_executor(language: str) -> Executor:
        if language == "PYTHON":
            return PythonExecutor()
        if language == "C":
            return CExecutor()
        if language == "CPP":
            return CppExecutor()
        if language == "JAVA":
            return JavaExecutor()

        raise ValueError("Unsupported language")