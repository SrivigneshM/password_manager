#!/bin/bash

# shellcheck source=env.sh
. env.sh

# shellcheck disable=SC2006,SC2046,SC2166,SC2050,SC2148
source ENV/bin/activate

pip3 install -r requirements.txt
pip3 install -r test-requirements.txt

sqlite3 test_password_manager.db ".quit"

lockutils-wrapper pytest "$@"
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
