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


def test_calculator_add(client):
    response = client.get('/calculator', query_string={'operator': 'plus', 'operand1': 2, 'operand2': 2})
    assert response.status_code == 200
    assert '4' in response.data


def test_calculator_minus(client):
    response = client.get('/calculator', query_string={'operator': 'minus', 'operand1': 4, 'operand2': 2})
    assert response.status_code == 200
    assert '2' in response.data


def test_calculator_mult(client):
    response = client.get('/calculator', query_string={'operator': 'mult', 'operand1': 5, 'operand2': 2})
    assert response.status_code == 200
    assert '10' in response.data


def test_calculator_div(client):
    response = client.get('/calculator', query_string={'operator': 'div', 'operand1': 6, 'operand2': 2})
    assert response.status_code == 200
    assert '3' in response.data

