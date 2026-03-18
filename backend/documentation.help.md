# Guia de como utilizar a documentação de decorators do Flask/Swagger

* `@api.route("/routename")`

  * Cria uma rota no namespace com aquele determinado caminho.
  * A classe abaixo desse decorator será responsável por tratar as requisições desse endpoint.
  * Exemplo:

    ```py
    @api.route("/users")
    class UserList(Resource):
        def get(self):
            pass
    ```

* `@api.expect(model)`

  * Define qual modelo de dados a requisição espera receber.
  * Esse modelo normalmente é definido com `api.model`.
  * Usado principalmente para `POST`, `PUT` e `PATCH`.
  * Também serve para gerar automaticamente a documentação no Swagger.
  * Exemplo:

    ```py
    @api.expect(UserCreateModel, validate=True)
    def post(self):
        pass
    ```

* `@api.expect(model, validate=True)`

  * Faz a validação automática do payload recebido.
  * Se o JSON enviado não corresponder ao modelo esperado, a API retorna erro `400` automaticamente.

* `@api.marshal_with(model)`

  * Define como a resposta será serializada antes de ser enviada ao cliente.
  * O retorno do método será transformado para seguir o formato do modelo definido.
  * Exemplo:

    ```py
    @api.marshal_with(UserModel)
    def get(self):
        return user
    ```

* `@api.marshal_list_with(model)`

  * Igual ao `marshal_with`, porém utilizado quando o retorno é uma lista de objetos.
  * Exemplo:

    ```py
    @api.marshal_list_with(UserModel)
    def get(self):
        return users
    ```

* `@api.response(status_code, description)`

  * Documenta possíveis respostas HTTP do endpoint.
  * Isso aparece automaticamente na documentação Swagger.
  * Exemplo:

    ```py
    @api.response(200, "Usuário encontrado")
    @api.response(404, "Usuário não encontrado")
    ```

* `@api.doc(...)`

  * Permite adicionar metadados ao endpoint na documentação.
  * Pode definir descrição, parâmetros, tags, entre outros.
  * Exemplo:

    ```py
    @api.doc(description="Atualiza os dados de um usuário")
    ```

* `@api.param(name, description)`

  * Define parâmetros utilizados pela rota.
  * Muito usado para parâmetros de URL ou query.
  * Exemplo:

    ```py
    @api.param("id", "ID do usuário")
    ```

* `@api.header(name, description)`

  * Documenta headers esperados na requisição.
  * Exemplo comum: token de autenticação.
  * Exemplo:

    ```py
    @api.header("Authorization", "Token JWT")
    ```

* `@api.deprecated`

  * Marca o endpoint como obsoleto na documentação.
  * Indica que aquele endpoint não deve mais ser utilizado.

* `@api.hide`

  * Remove o endpoint da documentação Swagger.
  * A rota continua funcionando normalmente, apenas não aparece na documentação.

* `@api.produces(content_types)`

  * Define quais tipos de conteúdo o endpoint pode retornar.
  * Exemplo:

    ```py
    @api.produces(["application/json"])
    ```

* `@api.consumes(content_types)`

  * Define quais tipos de conteúdo o endpoint aceita na requisição.
  * Exemplo:

    ```py
    @api.consumes(["application/json"])
    ```

* `@api.security(name)`

  * Define qual esquema de segurança o endpoint utiliza.
  * Normalmente usado para autenticação com API Key ou JWT.
  * Exemplo:

    ```py
    @api.security("apikey")
    ```

## Exemplo completo

```py
@api.route("/users/<int:id>")
class UserResource(Resource):

    @api.doc(description="Atualiza um usuário")
    @api.param("id", "ID do usuário")
    @api.expect(UserUpdateModel, validate=True)
    @api.marshal_with(UserModel)
    @api.response(200, "Usuário atualizado com sucesso")
    @api.response(404, "Usuário não encontrado")
    def put(self, id):
        pass
```
