#!/bin/bash

# shellcheck source=env.sh
. env.sh

# shellcheck disable=SC2006,SC2046,SC2166,SC2050,SC2148
source ENV/bin/activate

pip3 install -r requirements.txt

sqlite3 "password_manager.db" ".read schema.sql"

# circusd --daemon "${HOME_DIR}"/circus/circus.ini
nohup python3 "${SRC_DIR}"/webapps/app.py >/dev/null 2>&1 &
