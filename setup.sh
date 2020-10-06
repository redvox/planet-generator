#!/usr/bin/env bash
set -e

if [ ! -d venv ]; then
    pip3.8 install --user virtualenv
    python3.8 -m virtualenv -p python3 venv
fi

./venv/bin/pip3 install -r requirements.txt
