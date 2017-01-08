#!/bin/bash

# Get absolute path of the script.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
ROOT_PATH=$( cd "$(dirname "${PARENT_PATH}")" ; pwd -P )

cd "$ROOT_PATH/translate"

echo "** Starting Gunicorn..."
gunicorn --config translate/gunicorn.py translate.wsgi
