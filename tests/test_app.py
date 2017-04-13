import pytest

from workshop import app


@pytest.fixture()
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    return client


def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Hello' in response.data and 'world' in response.data


def test_add(client):
    response = client.get('/add', query_string={'operand1': 2, 'operand2': 2})
    assert response.status_code == 200
    assert '4' in response.data

