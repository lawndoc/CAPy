import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-default-key"
    CA_CERT_DIR = os.environ.get("CA_CERT_DIR") or "/opt/CAPy/CA/"
    HOST_CERT_DIR = os.environ.get("HOST_CERT_DIR") or "/opt/CAPy/host/"
    CLIENT_CERT_DIR = os.environ.get("CLIENT_CERT_DIR") or "/opt/CAPy/client/"
