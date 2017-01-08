import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# settings ex. translate.settings.production
settings = os.environ.get('DJANGO_SETTINGS_MODULE')
raw_env = 'DJANGO_SETTINGS_MODULE={}'.format(settings)

HOST = '127.0.0.1'

PORT = '8000'

bind = '{}:{}'.format(HOST, PORT)

accesslog = '/vagrant/logs/gunicorn/gunicorn-access.log'

errorlog = '/vagrant/logs/gunicorn/gunicorn-error.log'

workers = 1

reload = True

daemon = True
