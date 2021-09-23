from api import app
import json
import pytest
import requests

@pytest.fixture
def client():
    app.testing = True
    yield app.test_client()

@pytest.fixture
def startWebServer():
    pass  #TODO

def testHostCert(client):
    response = client.get("/ca/host-certificate",
                          headers={"Content-Type": "application/json"},
                          data=json.dumps({"hostname": "testhost.local"}))
    hostKey = response.json()["key"]
    hostCert = response.json()["cert"]
    rootCert = response.json()["root"]

    response = requests.get("http://127.0.0.1:8443/",
                            cert=(hostCert, hostKey),
                            verify=rootCert)
    assert response.status_code == 200