import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-default-key"
    CA_CERT_DIR = os.environ.get("CA_CERT_DIR") or "/opt/CAPy/CA/"
    CA_NAME = os.environ.get("CA_NAME") or "CAPy Root CA"