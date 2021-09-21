from api import app
import pytest
import requests

@pytest.fixture
def client():
    app.testing = True
    yield app.test_client()

def testRootCert(client):
    response = client.get("/ca/root-trust")
    assert response.status_code == 200
    assert "root" in response.json()


def testHostCert(client):
    response = client.get("/ca/host-certificate",
                                 data={"host": "testhost.local"})
    assert response.status_code == 200
    assert "key" in response.json()
    assert "cert" in response.json()
    assert "root" in response.json()
    # hostKey = response.json()["key"]
    # hostCert = response.json()["cert"]
    # rootCert = response.json()["root"]

    # response = requests.get("http://127.0.0.1:8443/",
    #                         cert=(hostCert, hostKey),
    #                         verify=rootCert)
    # assert response.status_code == 200

