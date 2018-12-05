# MySQL Backup to AWS S3

Este script realiza o dump de um banco de dados MySQL e envia o arquivo zipado para o Amazon S3.

## Requerimentos

- Python 3.5
- MySQL Dump

## Desenvolvimento

**IMPORTANTE:** É necessário ter o Python 3.5 instalado. 
Para instalar no macOS use: `brew install python3`.
Para instalar no Linux Ubuntu use: `sudo apt-get install python3.5`

- Instale o gerenciador de dependencias `pipenv`

```sh
pip install pipenv
```

- Instale as dependências do projeto

```sh
pipenv install
```

- Instale o `mysqldump`

```sh
sudo apt-get install mysql-client
```

[virtual-env]: https://docs.python-guide.org/dev/virtualenvs/