#!/bin/bash

python3 -m venv ENV

HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHONBIN=${HOME_DIR}/ENV/bin
SRC_DIR=${HOME_DIR}/src
export PYTHONPATH=$HOME_DIR:$PYTHONBIN:$SRC_DIR

"${PYTHONBIN}"/pip3 install -r requirements.txt

sqlite3 "password_manager.db" ".read schema.sql"

nohup "${PYTHONBIN}"/uwsgi --http :5000 --wsgi-file "${SRC_DIR}"/webapps/app.py --callable app >/dev/null 2>&1 &
