## Métodos de Projeto de Software - Projeto

Esse repositório contém o código desenvolvido para o projeto da disciplina de Métodos de Projeto de Software, ministrada na Universidade Federal da Paraíba (UFPB). O trabalho em questão, chamado **Red Balloon**, propõe a criação de um sistema de interação e aprendizado de código no qual usuários podem criar e/ou resolver problemas de programação, engajando em um debate por soluções melhores em um sistema de fórum com outros usuários e participando de salas virtuais para a resolução em tempo real de um conjunto de questões.

**Observação:** o projeto está sendo desenvolvido de forma incremental e será atualizado após sprints semanais, que adicionarão mais funcionalidades e interações ao sistema proposto.

### Funcionalidades

- Diagrama de casos de uso e diagrama de análise de classes para modelagem do sistema de gerenciamento de usuário do projeto;

- Implementação de funções de CRUD para usuários, permitindo **adição**, **remoção**, **atualização** e **visualização total** de usuários (definida no diretório `\backend\user`).

## Intruções de uso

1. Faça uma cópia local desse repositório na sua máquina.

```bash
git clone "https://github.com/sunny-fellow/RedBalloon"
```

2. Com o terminal aberto no diretório `RedBalloon\backend`, rode o seguinte comando para adquirir todos os requisitos para a execução do projeto.

```bash
pip install -r requirements.txt
```

3. Após isso, no mesmo diretório, inicie a aplicação.

```bash
py main.py
```

4. Após o servidor iniciar, abra o endereço web determinado e adicione o endpoint `/apidocs` para acessar a API, como no exemplo abaixo:

```plaintext
http://127.0.0.1:5000/apidocs
```

5. Use as funcionalidades de CRUD implementadas por meio do Swagger.