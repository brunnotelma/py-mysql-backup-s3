# MySQL Backup to AWS S3

Este script realiza o dump de um banco de dados MySQL e envia o arquivo zipado para o Amazon S3.

## Requerimentos

- Python 3
- MySQL Dump

## Desenvolvimento

**IMPORTANTE:** É necessário ter o Python 3.7 instalado. Para instalar no macOS use: `brew install python3`.

- Instale o gerenciador de dependencias `pipenv`

```sh
pip install pipenv
```

- Instale as dependências do projeto

```sh
pipenv install
```

[virtual-env]: https://docs.python-guide.org/dev/virtualenvs/