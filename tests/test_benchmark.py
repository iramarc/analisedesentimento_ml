import time
import requests

API_URL = "http://127.0.0.1:5000/predict"
TEST_TEXT = "I am feeling great!"
MAX_RESPONSE_TIME = 0.2  # Tempo limite em segundos

def test_benchmark():
    start_time = time.time()
    response = requests.post(API_URL, json={"text": TEST_TEXT})
    end_time = time.time()

    assert response.status_code == 200, f"Erro no servidor: {response.status_code} - {response.text}"
    elapsed_time = end_time - start_time
    print(f"Tempo de resposta: {elapsed_time:.3f} segundos")
    assert elapsed_time <= MAX_RESPONSE_TIME, "Tempo de resposta excedeu o limite!"

if __name__ == "__main__":
    test_benchmark()

