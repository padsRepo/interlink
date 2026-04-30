#!/bin/bash

BASE_DIR=$(dirname "$(readlink -f "${0%/*}")")

cd "${BASE_DIR}/tests/dev"
. .env
. venv/bin/activate
python __init__.py