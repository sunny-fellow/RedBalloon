## Métodos de Projeto de Software - Projeto

Esse repositório contém o código desenvolvido para o projeto da disciplina de Métodos de Projeto de Software, ministrada na Universidade Federal da Paraíba (UFPB). O trabalho em questão, chamado **Red Balloon**, propõe a criação de um sistema de interação e aprendizado de código no qual usuários podem criar e/ou resolver problemas de programação, engajando em um debate por soluções melhores em um sistema de fórum com outros usuários e participando de salas virtuais para a resolução em tempo real de um conjunto de questões.

**Observação:** o projeto está sendo desenvolvido de forma incremental e será atualizado após sprints semanais, que adicionarão mais funcionalidades e interações ao sistema proposto.

### Documentos (todos encontrados no diretório `docs`)

- Documento de requisitos;
- Diagrama de classes de análise (versão 1 e versão 2);
- Modelagem do banco de dados por meio do diagrama entidade-relacionamento;
- Diagrama de casos de uso para CRUD de usuários.

### Funcionalidades

- Implementação de funções de CRUD para usuários, permitindo **adição**, **remoção**, **atualização** e **visualização total** de usuários (definida no diretório `backend/user`);
- Verificação de login e senha, segundo padrões propostos pela atividade;
- Implementação de armazenamento de memória persistente, usando JSON.

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

3. **Frontend (Node - Vite - React - Typescript)**

    3.1. Em um novo terminal, navegue até o diretório `frontend`
    ```bash
    cd frontend
    ```

    3.2. Instale todas as dependências necessárias
    ```bash
    npm install
    npm audit fix
    ```

    3.3. Rode o frontend
    ```bash
    npm start 
    ```

4. Após o servidor iniciar, abra o endereço web determinado e adicione o endpoint `/apidocs` para acessar a API, por exemplo:

```plaintext
http://127.0.0.1:5000/apidocs
```

5. Use as funcionalidades de CRUD e demais endpoints por meio do Swagger.

```

Se você quiser, posso adicionar também **instruções para rodar frontend + backend simultaneamente no Windows/WSL**, sem precisar de scripts externos. Isso deixa o README pronto para novos usuários. Quer que eu faça?
```
