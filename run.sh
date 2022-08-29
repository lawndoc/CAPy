#!/usr/bin/with-contenv bash

# initialize CA files before multithreading
python3.9 init_CAPy.py --proxy ${PROXY_DOMAIN}

# start async flask service
gunicorn -b 0.0.0.0:5000 -w 2 -k gevent --worker-tmp-dir /dev/shm api:app