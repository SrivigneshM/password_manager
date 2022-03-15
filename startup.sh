#!/bin/bash

python3 -m venv ENV

HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHONBIN=${HOME_DIR}/ENV/bin
SRC_DIR=${HOME_DIR}/src
export PYTHONPATH=$HOME_DIR:$PYTHONBIN:$SRC_DIR

pip3 install -r requirements.txt

sqlite3 "password_manager.db" ".read schema.sql"

circusd --daemon "${HOME_DIR}"/circus/circus.ini
