import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOST = '127.0.0.1'

PORT = '8000'

bind = '{}:{}'.format(HOST, PORT)

accesslog = '/var/log/gunicorn/access.log'

errorlog = '/var/log/gunicorn/error.log'

workers = 1

reload = True

daemon = True
