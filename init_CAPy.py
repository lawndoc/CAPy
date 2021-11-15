import argparse
from config import Config
from ownca import CertificateAuthority

# initialize CA if it doesn't exist
ca = CertificateAuthority(ca_storage=Config.CA_CERT_DIR, common_name=Config.CA_NAME)

# generate intial host certificate for the frontend
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--frontend",
                    help="fqdn of the frontend to generate a certificate",
                    default="example.com",
                    type=str)
args = parser.parse_args()
ca.issue_certificate(hostname=args.frontend,
                     maximum_days=825,
                     common_name=args.frontend,
                     dns_names=[],
                     oids={},
                     public_exponent=65537,
                     key_size=2048)

# done, exit back to script
exit()
