#!/bin/bash

# shellcheck source=env.sh
. env.sh

pip3 install --use-deprecated=legacy-resolver -r requirements.txt

sqlite3 "password_manager.db" ".read schema.sql"

circusd --daemon "${HOME_DIR}"/circus/circus.ini
