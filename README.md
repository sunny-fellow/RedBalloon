#  Red Balloon - Backend

## Sobre o Projeto

Este repositório contém o sistema **Red Balloon**, desenvolvido na disciplina de **Métodos de Projeto de Software** da Universidade Federal da Paraíba (UFPB). O sistema propõe um ambiente de interação e aprendizado em programação, no qual usuários podem:

- Criar e resolver problemas de programação
- Discutir soluções em formato de fórum
- Participar de salas virtuais para resolução colaborativa em tempo real

O desenvolvimento segue um **modelo incremental**, com evolução contínua a cada sprint semanal, adicionando novas funcionalidades progressivamente.

> **Observação:** Devido ao escopo requerido, as funcionalidades do sistema estão completamente funcionais via API, mas não há integração com interface gráfica (frontend).

---

##  Evolução do Projeto

As entregas foram estruturadas de forma incremental, adicionando funcionalidades progressivamente:

| Sprint | Funcionalidades Adicionadas |
|--------|----------------------------|
| **1ª Entrega** | • Modelagem inicial com diagrama de classes<br>• CRUD básico para entidade `User` |
| **2ª Entrega** | • Persistência de dados em memória (JSON)<br>• Validação de credenciais de login |
| **3ª Entrega** | • Nova entidade `Problem` com operações CRUD<br>• Padrões **Facade** e **Singleton** para gerenciar Controllers |
| **4ª Entrega** | • Separação das camadas de negócio e persistência (Repositories/Services)<br>• Padrão **Abstract Factory** para criação de repositórios<br>• Padrão **Adapter** para sistema de logs<br>• Padrão **Template Method** para relatórios de acesso |
| **5ª Entrega** | • Atualização da fachada com padrão **Command**<br>• Padrão **Memento** para desfazer atualizações no banco |
| **6ª Entrega** | • Padrões **Strategy** (execução de código) e **Observer** (eventos)<br>• Documentação e modelagem completa do sistema |

---

### Documentos (todos encontrados no diretório `docs`)
A seção de documentos contém todo o conjunto de documentos escritos e validados em algumas das entregas. Cada versão está armazenada em um diretório próprio, mas a versão final encontra-se na raiz desssa seção e contém os seguintes artefatos:

- Documento de requisitos atualizado;
- Diagrama de classes completo com a marcação de cada padrão usado;
- Documentação dos padrões usados e seu objetivo no código.


## Instruções de uso

1. Faça uma cópia local desse repositório na sua máquina:

```bash
git clone "https://github.com/sunny-fellow/RedBalloon"
```

2. **Backend (Windows + WSL ou Linux)** 

    2.1. Abra um terminal no diretório `RedBalloon/backend` e crie um ambiente virtual:

    ```bash
    python3 -m venv venv
    ```

    2.2. Ative o ambiente virtual:

    ```bash
    source venv/bin/activate
    ```

    2.3. Instale os requisitos do projeto:

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

    2.4. Inicie a aplicação:

    ```bash
    python main.py
    ```

4. Após o servidor iniciar, abra o endereço web determinado e adicione o endpoint `/apidocs` para acessar a API, por exemplo:

```plaintext
http://127.0.0.1:5000/apidocs
```

5. Use as funcionalidades de CRUD e demais endpoints por meio do Swagger.
