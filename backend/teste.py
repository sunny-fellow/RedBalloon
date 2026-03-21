from execution.executors.java_executor import JavaExecutor
from execution.executors.python_executor import PythonExecutor
from execution.executors.cpp_executor import CppExecutor
from execution.executors.c_executor import CExecutor

def run_test(name, executor, code, input_data=""):
    print(f"\n===== TESTE: {name} =====")
    try:
        result = executor.execute(code, input_data, 2000, 128)
        print(result)
    except Exception as e:
        print("ERRO NO TESTE:", str(e))


# ---------------- PYTHON ----------------

py_exec = PythonExecutor()

run_test("Python - Loop infinito", py_exec, """
while True:
    pass
""")

run_test("Python - Memória", py_exec, """
a = []
while True:
    a.append("A" * 10**6)
""")

run_test("Python - Arquivo sistema", py_exec, """
print(open("/etc/passwd").read())
""")

run_test("Python - Escrita arquivo", py_exec, """
with open("hack.txt", "w") as f:
    f.write("hacked")
print("done")
""")

run_test("Python - Rede", py_exec, """
import socket
s = socket.socket()
s.connect(("google.com", 80))
""")

run_test("Python - Exec sistema", py_exec, """
import os
os.system("ls /")
""")


# ---------------- JAVA ----------------

java_exec = JavaExecutor()

run_test("Java - OK", java_exec,
"public class Solution { public static void main(String[] args){ System.out.println(\"OK\"); } }"
)

run_test("Java - Loop infinito", java_exec,
"public class Solution { public static void main(String[] args){ while(true){} } }"
)

run_test("Java - Memória", java_exec,
"""
import java.util.*;
public class Solution {
    public static void main(String[] args){
        List<byte[]> list = new ArrayList<>();
        while(true){
            list.add(new byte[1024 * 1024]);
        }
    }
}
"""
)

run_test("Java - Ler sistema", java_exec,
"""
import java.io.*;
public class Solution {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new FileReader("/etc/passwd"));
        System.out.println(br.readLine());
    }
}
"""
)

run_test("Java - Escrita", java_exec,
"""
import java.io.*;
public class Solution {
    public static void main(String[] args) throws Exception {
        FileWriter fw = new FileWriter("/tmp/hack.txt");
        fw.write("hack");
        fw.close();
        System.out.println("done");
    }
}
"""
)


# ---------------- C ----------------

c_exec = CExecutor()

run_test("C - Loop infinito", c_exec, """
int main() {
    while(1){}
    return 0;
}
""")

run_test("C - NORMAL", c_exec, """        
    #include <stdio.h>
    #include <unistd.h>
    int main() {
        printf("OLA");
        return 0;
    }
    """)

run_test("C - Ler sistema", c_exec, """
#include <stdio.h>
int main() {
    FILE *f = fopen("/etc/passwd", "");
    if (f) {
        char c;
        while ((c = fgetc(f)) != EOF) putchar(c);
    }
    return 0;
}
""")


# ---------------- C++ ----------------

cpp_exec = CppExecutor()

run_test("C++ - Loop infinito", cpp_exec, """
int main() {
    while(true){}
}
""")

run_test("C++ - Memória", cpp_exec, """
#include <vector>
using namespace std;
int main() {
    vector<string> v;
    while(true) {
        v.push_back(string(1000000, 'A'));
    }
}
""")