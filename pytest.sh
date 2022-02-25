#!/bin/bash

SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHONBIN=${SRC_DIR}/ENV/bin
export PYTHONPATH=$SRC_DIR:$PYTHONBIN


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
