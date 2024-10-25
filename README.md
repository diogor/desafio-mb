# Quero Ser MB - Teste Backend 3
Consiste em uma API que retorna a cotação para o símbolo de um ativo.

## Requisitos
- Python 3.11 ou superior
- Make
- Virtualenv
    - Poetry (https://python-poetry.org/) (Recomendado)
    - Pipenv (https://pipenv.pypa.io/)
    - Ou outra maneira de intalar um virtualenv:
      - Ex:
        ```sh
        python3 -m venv .venv
        ```

## Instalação
- Poetry:
    - `poetry install`
- Ou ative seu virtualenv:
    ```sh 
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## Configuração
- Copie o arquivo `.env.example` para `.env`
- Modifique as variáveis de ambiente do arquivo `.env` de acordo com suas necessidades, ou siga com o padrão.

### Configuração da aplicação (opcional)
Como é necessário chamar outra api que não a do MB, e elas são diferentes tanto na url quanto na resposta,
achei que valia a pena usar uma configuração padronizada para ser fácil utilizar qualquer estrutura de API.
- Dentro do diretório `config/`, existem 2 arquivos `.ini`:
    - `apis.ini`: Configurações das apis de consulta.
    - `symbols.ini`: Configurações dos ativos disponíveis.

## Rodando
- Ative o seu **virtualenv** ou rode os comandos a seguir com seu gerenciador de dependências:
### Migração de dados
Devido ao sistema básico de autenticação, é necessário uma migração de banco.
- Utilizando poetry:
    ```sh
    poetry run make migrate
    ```
- Ou utilizando o virtualenv:
    ```sh
    source .venv/bin/activate
    make migrate
    ```
### Rodando a aplicação
Pode ser iniciada com parâmetros adicionais de porta e host: `port=<port>` e `host=<ip>`
- Utilizando poetry:
    ```sh
    poetry run make api
    ```
- Ou utilizando o virtualenv:
    ```sh
    source .venv/bin/activate
    make api
    ```
### Interface de documentação (swagger)
A documentação básica da api pode ser acessada na URL: `/docs`
