#!/bin/bash

SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHONBIN=${SRC_DIR}/ENV/bin
export PYTHONPATH=$SRC_DIR:$PYTHONBIN

"${PYTHONBIN}"/lockutils-wrapper "${PYTHONBIN}"/pytest "$@"
