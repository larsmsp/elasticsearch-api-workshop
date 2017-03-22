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


def test_greet_query_string(client):
    response = client.get('/greet', query_string={'name': 'My Name'})
    assert response.status_code == 200
    assert 'My Name' in response.data


def test_greet_endpoint(client):
    response = client.get('/resource/my-id')
    assert response.status_code == 200
    assert 'my-id' in response.data
