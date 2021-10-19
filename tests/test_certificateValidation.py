import json
from OpenSSL import crypto

def testValidHostCert(client):
    # request new host certificate
    response = client.get("/ca/host-certificate",
                          headers={"Content-Type": "application/json"},
                          data=json.dumps({"hostname": "testhost.local"}))
    assert response.status_code == 200
    # get host and root certs from the response
    hostCert = crypto.load_certificate(crypto.FILETYPE_PEM, response.json["cert"])
    rootCert = crypto.load_certificate(crypto.FILETYPE_PEM, response.json["root"])
    # add root cert to trusted certs
    store = crypto.X509Store()
    store.add_cert(rootCert)
    # create cert store context and validate host cert
    store_ctx = crypto.X509StoreContext(store, hostCert)
    assert store_ctx.verify_certificate() == None
