import os
import time
import datetime
import pipes
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAMES = os.getenv('DB_NAMES').split(',')
BACKUP_PATH = os.getenv('BACKUP_PATH') + '/' + time.strftime('%Y%m')

# Testa se a pasta existe
try:
    os.stat(BACKUP_PATH)
except:
    # Se nao existir, cria a pasta
    os.mkdir(BACKUP_PATH)

# Realiza o backup de todos os databases
for db in DB_NAMES:
    FILE_NAME = db + '_' + time.strftime('%Y%m%d-%H%M%S') + '.sql'
    FILE_PATH = pipes.quote(BACKUP_PATH) + "/" + FILE_NAME

    dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + \
        DB_PASSWORD + " " + db + " > " + FILE_PATH
    os.system(dumpcmd)

    gzipcmd = "gzip " + FILE_PATH
    os.system(gzipcmd)

print('Backup criado com sucesso!')
