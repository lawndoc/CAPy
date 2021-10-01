from config import Config
from ownca import CertificateAuthority

# initialize CA if it doesn't exist and exit
ca = CertificateAuthority(ca_storage=Config.CA_CERT_DIR, common_name=Config.CA_NAME)
exit()
