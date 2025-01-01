import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    """Testa a rota principal"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'<title>ML Sentiment Analysis</title>' in rv.data  # Alterado para o título correto

def test_predict(client):
    """Testa a rota de predição"""
    rv = client.post('/predict', json={'text': 'I am feeling great!'})
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'prediction' in json_data
    assert 'confidence' in json_data
