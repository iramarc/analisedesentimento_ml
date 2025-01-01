import time
import requests

API_URL = "http://127.0.0.1:5000/predict"
TEST_TEXT = "I am feeling great!"
MAX_RESPONSE_TIME = 0.2  # Tempo limite em segundos

def benchmark():
    try:
        start_time = time.time()
        response = requests.post(API_URL, json={"text": TEST_TEXT})
        end_time = time.time()

        if response.status_code == 200:
            elapsed_time = end_time - start_time
            print(f"Tempo de resposta: {elapsed_time:.3f} segundos")
            
            if elapsed_time > MAX_RESPONSE_TIME:
                print("Falha: Tempo de resposta excedeu o limite!")
                exit(1)
            else:
                print("Sucesso: Tempo de resposta dentro do limite!")
        else:
            print(f"Erro no servidor: {response.status_code} - {response.text}")
            exit(1)
    except Exception as e:
        print(f"Erro ao executar benchmark: {e}")
        exit(1)

if __name__ == "__main__":
    benchmark()