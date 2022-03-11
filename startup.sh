#!/bin/bash

HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHONBIN=${HOME_DIR}/ENV/bin
SRC_DIR=${HOME_DIR}/src
export PYTHONPATH=$HOME_DIR:$PYTHONBIN:$SRC_DIR


sqlite3 "password_manager.db" ".read schema.sql"

nohup python3 src/webapps/app.py >/dev/null 2>&1 &
