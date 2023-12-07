import pytest
from app import app
from src.models import db

@pytest.fixture(scope='module')
def test_app():
    
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    yield app.test_client()  

    db.session.remove()
    db.drop_all()
    app_context.pop()