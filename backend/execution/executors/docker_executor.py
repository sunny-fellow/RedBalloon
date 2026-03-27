import docker
import tempfile
import shutil
import os
import time
import threading
from models.enums import SubmissionStatus

class DockerExecutor:
    def __init__(self, image: str):
        self.client = docker.from_env()
        self.image = image

    def _get_config(self, language: str, memory_limit_mb: int):
        lang = language.lower()
        if lang == "python":
            return {"filename": "Main.py", "command": "python3 /sandbox/Main.py < /sandbox/input.txt", "pids": 8}
        elif lang == "java":
            # Modo Java 11+ (Source File Mode): compila em memória e roda direto
            java_policy = '-Djava.security.manager -Djava.security.policy==/sandbox/security.policy'
            return {"filename": "Solution.java", "command": f"java {java_policy} -Xmx{memory_limit_mb}m /sandbox/Solution.java < /sandbox/input.txt", "pids": 64}
        elif lang in ("c", "cpp"):
            compiler = "gcc" if lang == "c" else "g++"
            filename = "Main." + lang 
            # Compila no /tmp (RAM) e executa. O 'chmod' não é estritamente necessário se rodar via /tmp montado com exec.
            return {
                "filename": filename,
                "command": f"{compiler} /sandbox/{filename} -O2 -o /tmp/main_binary && /tmp/main_binary < /sandbox/input.txt",
                "pids": 8
            }
        else:
            raise ValueError(f"Unsupported language: {language}")

    def execute(self, source_code, input_data, time_limit_ms, memory_limit_mb, language: str):
        tmp_dir = tempfile.mkdtemp()
        sandbox_path = os.path.join(tmp_dir, "sandbox")
        os.makedirs(sandbox_path, exist_ok=True)

        config = self._get_config(language, memory_limit_mb)
        # Inicializamos como erro desconhecido; será atualizado conforme o fluxo
        result = {"status": SubmissionStatus.RUNTIME_ERROR, "output": "", "error": "", "time_spent_ms": 0}
        container = None
        
        try:
            with open(os.path.join(sandbox_path, config["filename"]), "w", encoding="latin-1") as f:
                f.write(source_code)
            with open(os.path.join(sandbox_path, "input.txt"), "w", encoding="latin-1") as f:
                f.write(input_data)
        except Exception as e:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return {"status": SubmissionStatus.RUNTIME_ERROR, "error": f"Setup error: {str(e)}"}

        start_time = time.perf_counter()

        try:
            container = self.client.containers.run(
                image=self.image,
                command=["sh", "-c", config["command"]],
                volumes={sandbox_path: {"bind": "/sandbox", "mode": "ro"}},
                working_dir="/sandbox",
                user="1000:1000",
                network_disabled=True,
                read_only=True,
                security_opt=["no-new-privileges"],
                cap_drop=["ALL"],
                tmpfs={"/tmp": "rw,exec,nosuid,nodev,size=32m"},
                mem_limit=f"{memory_limit_mb}m",
                memswap_limit=f"{memory_limit_mb}m",
                cpu_period=100000,
                cpu_quota=50000,
                pids_limit=config["pids"],
                # Limite de stack para evitar estouro proposital (8MB padrão)
                ulimits=[docker.types.Ulimit(name="stack", soft=8192000, hard=8192000)],
                detach=True
            )

            # Aguarda o container com timeout manual para precisão do TLE
            try:
                exit_info = container.wait(timeout=time_limit_ms / 1000)
                exit_code = exit_info["StatusCode"]
            except:
                # Se cair aqui, o timeout do wait estourou (TLE)
                try: container.kill()
                except: pass
                result["status"] = SubmissionStatus.TIME_LIMIT_EXCEEDED
                return self._finalize(container, result, start_time, tmp_dir)

            # Pega logs e verifica se houve estouro de memória (OOM)
            container.reload() # Atualiza dados do container
            is_oom = container.attrs['State'].get('OOMKilled', False)
            logs = container.logs(stdout=True, stderr=True).decode()
            
            if len(logs) > 10000:
                logs = logs[:10000] + "\n...[truncated]"

            # Lógica de decisão de Status
            if is_oom:
                result.update({"status": SubmissionStatus.MEMORY_LIMIT_EXCEEDED, "error": "Memory limit exceeded."})
            elif exit_code == 137: # Container morto externamente (geralmente TLE/SIGKILL)
                result.update({"status": SubmissionStatus.TIME_LIMIT_EXCEEDED})
            elif exit_code != 0:
                result.update({"status": SubmissionStatus.RUNTIME_ERROR, "error": logs})
            else:
                result.update({"status": SubmissionStatus.ACCEPTED, "output": logs})

        except Exception as e:
            result.update({"status": SubmissionStatus.RUNTIME_ERROR, "error": str(e)})
        
        return self._finalize(container, result, start_time, tmp_dir)

    def _finalize(self, container, result, start_time, tmp_dir):
        """Limpa recursos e calcula tempo final."""
        result["time_spent_ms"] = int((time.perf_counter() - start_time) * 1000)
        
        if container:
            try: container.remove(force=True)
            except: pass
        
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return result