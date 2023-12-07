import pytest
from app.app import app

@pytest.fixture(scope='module')
def test_client():
    return app.test_client()