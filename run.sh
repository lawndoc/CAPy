#!/bin/sh

# add virtualenv to PATH
export VIRTUAL_ENV=/home/abc/venv
export PATH="/home/abc/venv/bin:$PATH"

# initialize CA files before multithreading
python3.9 init_CAPy.py --proxy ${PROXY_DOMAIN}

# start async flask service
gunicorn -b 0.0.0.0:5000 -w 2 -k gevent --worker-tmp-dir /dev/shm api:app