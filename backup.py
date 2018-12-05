import os
import time
import datetime
import pipes
import boto3
import dotenv

# Carrega o arquivo .env
dotenv.load_dotenv()

# Carrega as informacoes do arquivo
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
# Nomes dos bancos de dados devem ser separados por virgula
DB_NAMES = os.getenv('DB_NAMES').split(',')
# Tabelas que serao ignoradas
DB_IGNORE_TABLES = os.getenv('DB_IGNORE_TABLES').split(',')
# Uma pasta com ano e mes eh criada na pasta de backup
BACKUP_PATH = os.getenv('BACKUP_PATH') + '/' + time.strftime('%Y%m')
# Nome do Vault a ser utilizado
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Testa se a pasta existe
try:
    os.stat(BACKUP_PATH)
except:
    # Se nao existir, cria a pasta
    os.mkdir(BACKUP_PATH)

# Cria o objeto do AWS S3
s3 = boto3.resource('s3')
s3_enabled = False

try:
    # Se um bucket for encontrado com o nome configurado
    if any(bucket.name == AWS_BUCKET_NAME for bucket in s3.buckets.all()):
        # AWS S3 configurado com sucesso
        s3_enabled = True
    else:
        print('Bucket nao encontrado.')
except:
    print('Credenciais invalidas para a AWS S3.')


# Realiza o backup de todos os databases
for db in DB_NAMES:
    # Nome do arquivo de backup .sql
    FILE_NAME = db + '_' + time.strftime('%Y%m%d-%H%M%S') + '.sql'
    # Nome do arquivo comprimido
    COMPRESSED_FILE_NAME = FILE_NAME + '.tar.gz'
    # Caminho totalmente qualificado do arquivo de destino
    FILE_PATH = pipes.quote(BACKUP_PATH) + '/' + FILE_NAME
    # Tabelas que serao ignoradas
    IGNORED_TABLES = ''

    for table in DB_IGNORE_TABLES:
        if db in table:
            IGNORED_TABLES += ' --ignore-table=' + table

    # Chama o processo do MySQL dump
    os.system('mysqldump -h ' + DB_HOST + ' -u ' + DB_USER + ' -p' +
              DB_PASSWORD + ' ' + db + IGNORED_TABLES + ' > ' + FILE_PATH)

    # Compacta o arquivo
    os.system('tar -czvf ' + COMPRESSED_FILE_NAME + ' -C ' +
              pipes.quote(BACKUP_PATH) + ' ' + FILE_NAME)

    try:
        # Le os dados do arquivo
        file_data = open(COMPRESSED_FILE_NAME, 'rb')

        # Se o AWS S3 estiver configurado
        # corretamente, faz o upload do arquivo
        if s3_enabled:
            print('Enviando o arquivo %s para o AWS S3...' % FILE_NAME)
            # Faz o upload do arquivo para o Bucket configurado
            result = s3.Bucket(AWS_BUCKET_NAME).put_object(
                Key=COMPRESSED_FILE_NAME, Body=file_data)
            print(result)

        # Fecha o buffer do arquivo
        file_data.close()
    except:
        print('Falha ao criar arquivo de backup (%s).' % db)
