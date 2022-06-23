#!/bin/sh

# initialize CA files before multithreading
python3.9 init_CAPy.py --proxy ${PROXY_DOMAIN}

# start async flask service
gunicorn -b 0.0.0.0:5000 -w 4 -k gevent --worker-tmp-dir /dev/shm api:app