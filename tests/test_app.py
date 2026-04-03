import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.get_json()['message'] == 'Hello, World!'

def test_init_db(client):
    rv = client.get('/init_db')
    assert rv.status_code == 200
    assert rv.get_json()['status'] == 'initialized'
