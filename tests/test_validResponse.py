from api import app
import json
import pytest

@pytest.fixture
def client():
    app.testing = True
    yield app.test_client()
    

def testRootCert(client):
    response = client.get("/ca/root-trust")
    assert response.status_code == 200
    assert "root" in response.json


def testHostCert(client):
    response = client.get("/ca/host-certificate",
                          headers={"Content-Type": "application/json"},
                          data=json.dumps({"hostname": "testhost.local"}))
    assert response.status_code == 200
    assert "key" in response.json
    assert "cert" in response.json
    assert "root" in response.json

