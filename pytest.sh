#!/bin/bash

HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHONBIN=${HOME_DIR}/ENV/bin
SRC_DIR=${HOME_DIR}/src
export PYTHONPATH=$HOME_DIR:$PYTHONBIN:$SRC_DIR


sqlite3 test_password_manager.db ".quit"
"${PYTHONBIN}"/lockutils-wrapper "${PYTHONBIN}"/pytest "$@"
pytest_exit_code=$?
rm -rf test_password_manager.db
if [ ${pytest_exit_code} -eq 0 ]
then
  echo "pytest successful"
  exit 0
else
  echo "pytest failed"
  exit 1
fi
