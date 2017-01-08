import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

raw_env = 'DJANGO_SETTINGS_MODULE=translate.settings'

HOST = '0.0.0.0'

PORT = '8000'

bind = '{}:{}'.format(HOST, PORT)

accesslog = '/vagrant/logs/gunicorn/gunicorn-access.log'

errorlog = '/vagrant/logs/gunicorn/gunicorn-error.log'

workers = 1

reload = True

daemon = True
