from api import app
import pytest


@pytest.fixture
def client():
    app.testing = True
    yield app.test_client()