import os
from os.path import abspath, dirname, join
import sys

import django


def print_header():
    header = """
      _   _                                    _            _  _ 
   __| | (_)  __ _  _ __    __ _   ___    ___ | |__    ___ | || |
  / _` | | | / _` || '_ \  / _` | / _ \  / __|| '_ \  / _ \| || |
 | (_| | | || (_| || | | || (_| || (_) | \__ \| | | ||  __/| || |
  \__,_|_/ | \__,_||_| |_| \__, | \___/  |___/|_| |_| \___||_||_|
       |__/                |___/                                 
    """
    print(header)
    print("")


if __name__ == '__main__':
    path = join(dirname(dirname(abspath(__file__))), 'translate')
    print('path: {}'.format(path))

    sys.path.insert(0, abspath(path))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'translate.settings')
    django.setup()

    # Import Django modules.
    from django.conf import settings

    # Import models.
    from translation.models import *

    # Easy model functions.
    ph = lambda: Phrase.objects.all()
    tl = lambda: TranslateEvent.objects.all()

    print_header()
