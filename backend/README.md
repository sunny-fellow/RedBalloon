# RedBalloon Backend - Guia de Instalação
Este documento fornece as instruções necessárias para configurar o ambiente de desenvolvimento, construir os containers de execução e rodar o servidor.

## Pré-requisitos
Antes de começar, certifique-se de ter instalado em sua máquina:
* **Python 3.10+**
* **Docker** (essencial para os ambientes de execução de código)
* **Virtualenv** (recomendado)

## Passo 1: Configuração do Ambiente Python

1.  **Clone o repositório e acesse a pasta raiz:**
    ```bash
    cd backend
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Linux/MacOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Passo 2: Variáveis de Ambiente
Crie um arquivo `.env` na raiz do diretório `/backend` (ou na raiz do projeto, conforme sua estrutura) e preencha as seguintes chaves:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/redballoon
JWT_KEY=sua_chave_secreta_aqui
ADMIN_PASSWORD=sua_senha_admin_aqui
TOKEN_EXPIRATION_HOURS=24
```

## Passo 3: Construção das Imagens Docker (Ambientes de Execução)
O RedBalloon utiliza containers isolados para compilar e rodar submissões de código com segurança. Você **deve** buildar as imagens abaixo antes de iniciar o servidor:

```bash
# Navegue até a pasta de dockerfiles
cd backend/docker

# Build da imagem C
docker build -t sanbox-c ./c

# Build da imagem C++
docker build -t sanbox-cpp ./cpp

# Build da imagem Java
docker build -t sanbox-java ./java

# Build da imagem Python
docker build -t sanbox-python ./python
```

> **Nota:** Certifique-se de que os nomes das tags (`-t`) coincidem com o que o seu serviço de submissão espera encontrar ao instanciar os containers.

## Passo 4: Executando o Servidor
Com as dependências instaladas e as imagens Docker prontas, inicie o servidor Flask:

```bash
python backend/main.py
```

O servidor estará disponível em: `http://localhost:5000`

## Informações Úteis

### Documentação da API
A documentação interativa (Swagger) pode ser acessada em:
`http://localhost:5000/apidocs`

### Autenticação
1. Utilize o namespace `/auth` para realizar login e obter o seu **JWT**.
2. No Swagger, clique no botão **Authorize** e insira o token no formato: `Bearer SEU_TOKEN_AQUI`.
3. Todas as rotas (exceto as de autenticação e documentação) exigem este cabeçalho.
