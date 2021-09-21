from config import Config
from flask import Flask
from ownca import CertificateAuthority


app = Flask(__name__)
app.config.from_object(Config)

ca = CertificateAuthority(ca_storage=Config.CA_CERT_DIR, common_name=Config.CA_NAME)

from . import routes