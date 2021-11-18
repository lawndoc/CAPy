from api import app, ca
from flask import request
from ownca import utils
from ownca.exceptions import OwnCAInvalidCertificate


@app.get("/ca/root-trust")
def rootTrust():
    """ Return root CA certificate for setting up trust """
    cert = ca.cert_bytes.decode()
    return {"root": cert}


@app.get("/ca/host-certificate")
def getHostCertificate():
    """ Return an existing host certificate or create it if it doesn't exist """
    try:
        certHostname = request.json["hostname"]
        if not utils.validate_hostname(certHostname):
            raise ValueError
    except KeyError:
        return {"error": "hostname not found in the request"}, 400
    except ValueError:
        return {"error": "hostname in the request was not standard FQDN format"}, 400
    except TypeError:
        return {"error": "please ensure Content-Type is application/json"}, 400
    try:
        serverCert = ca.load_certificate(request.json["hostname"])
    except OwnCAInvalidCertificate:  # no certificate found, so create a new one
        certMaxDays = request.json.get("maxDays", 825)
        certCommonName = request.json.get("CN", request.json["hostname"])
        certDnsNames = request.json.get("DNS", [])
        certOids = {"country_name": request.json.get("C", ""),
                    "state_or_province": request.json.get("ST", ""),
                    "locality_name": request.json.get("L", ""),
                    "street_address": request.json.get("A", ""),
                    "organization_name": request.json.get("O", ""),
                    "organization_unit_name": request.json.get("OU", ""),
                    "email_address": request.json.get("E", "")}
        # remove blank OIDs to make ownca happy
        for oid in list(certOids.keys()):
            if not certOids[oid]:
                del certOids[oid]
        certPublicExponent = request.json.get("publicExponent", 65537)
        certKeySize = request.json.get("keySize", 2048)
        serverCert = ca.issue_certificate(hostname=certHostname,
                                        maximum_days=certMaxDays,
                                        common_name=certCommonName,
                                        dns_names=certDnsNames,
                                        oids=certOids,
                                        public_exponent=certPublicExponent,
                                        key_size=certKeySize)
    key = serverCert.key_bytes.decode()
    cert = serverCert.cert_bytes.decode()
    rootCert = ca.cert_bytes.decode()
    return {"key": key, "cert": cert, "root": rootCert}

# TODO: implement PEM certificate revocation
