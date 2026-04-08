## Métodos de Projeto de Software - Projeto
Este repositório contém o sistema Red Balloon, desenvolvido na disciplina de Métodos de Projeto de Software da Universidade Federal da Paraíba (UFPB). O sistema propõe um ambiente de interação e aprendizado em programação, no qual usuários podem criar e resolver problemas, discutir soluções em formato de fórum e participar de salas virtuais para resolução colaborativa em tempo real. O desenvolvimento segue um modelo incremental, com evolução contínua a cada sprint semanal, que adicionará mais funcionalidades ao sistema proposto.

**Observação:** devido ao escopo requerido, as funcionalidades do sistema estão completamente funcionais, mas não há integração com a interface gráfica (frontend).

## Evolução do Projeto
As entregas foram estruturadas de forma incremental, adicionando funcionalidades progressivamente.

### Primeira entrega
- Modelagem inicial do sistema por meio de diagrama de classes;
- Implementação de um CRUD básico para a entidade de usuários.

### Segunda entrega
- Implementação de persistência de dados em memória (JSON);
- Validação de credenciais de login.

### Terceira entrega
- Implementação de mais uma entidade, com operações de CRUD (problem);
- Adição de uma classe com os padrões Façade e Singleton, que gerencia os Controllers.

### Quarta entrega
- Separação das camadas de negócio e persistência do sistema (repositories e services);
- Implementação do padrão Abstract Factory para criação das entidades;
- Implementação do padrão Adapter para uso em sistemas de log;
- Adição do padrão Template Method para geração de relatórios de acesso ao sistema.

### Quinta entrega
- Atualização da fachada do sistema para uso do padrão Command;
- Implementação do padrão Memento para desfazer atualizações no banco de dados;

### Sexta entrega
- Adição de mais dois padrões de projeto: Strategy e Observer;
- Documentação e modelagem completa do sistema.

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
