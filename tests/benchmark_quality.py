import random
import json
from sklearn.metrics import classification_report
import requests

# Função para gerar dados sintéticos
def generate_synthetic_data(num_samples):
    positive_words = ["happy", "great", "amazing", "fantastic", "love"]
    negative_words = ["sad", "terrible", "awful", "hate", "bad"]
    synthetic_data = []
    
    for _ in range(num_samples):
        sentiment = random.choice(["POSITIVE", "NEGATIVE"])
        if sentiment == "POSITIVE":
            text = f"I am feeling {random.choice(positive_words)} today."
        else:
            text = f"I am feeling {random.choice(negative_words)} today."
        synthetic_data.append({"text": text, "expected": sentiment})
    
    return synthetic_data

def test_benchmark_quality():
    # Gerar dados sintéticos
    synthetic_data = generate_synthetic_data(100)  # Gerar 100 amostras sintéticas
    with open("synthetic_data.json", "w") as f:
        json.dump(synthetic_data, f, indent=4)
    print("Dados sintéticos gerados e salvos em synthetic_data.json")

    # Carregar dados de validação (incluindo os sintéticos)
    with open("validation_data.json", "r") as f:
        existing_data = json.load(f)

    combined_data = existing_data + synthetic_data

    # Preparar dados para avaliação
    true_labels = []
    predicted_labels = []

    for item in combined_data:
        text = item["text"]
        expected = item["expected"]
        true_labels.append(expected)
        
        # Fazer previsão com a API do app.py
        response = requests.post("http://127.0.0.1:5000/predict", json={"text": text})
        prediction = response.json()
        predicted_label = prediction["prediction"]
        print(f"Texto: {text} | Esperado: {expected} | Previsto: {predicted_label}")
        predicted_labels.append(predicted_label)

    # Calcular métricas
    report = classification_report(true_labels, predicted_labels, output_dict=True)

    # Exibir resultados
    print("Benchmarking de Qualidade de Inferência:")
    print(f"Precisão: {report['accuracy'] * 100:.2f}%")
    print(f"Recall (Positivo): {report['POSITIVE']['recall'] * 100:.2f}%")
    print(f"F1 Score (Positivo): {report['POSITIVE']['f1-score'] * 100:.2f}%")
    print(f"Recall (Negativo): {report['NEGATIVE']['recall'] * 100:.2f}%")
    print(f"F1 Score (Negativo): {report['NEGATIVE']['f1-score'] * 100:.2f}%")

    # Critérios de aceitação
    MIN_ACCURACY = 0.8
    if report["accuracy"] < MIN_ACCURACY:
        raise ValueError(f"A precisão do modelo está abaixo do limite aceitável de {MIN_ACCURACY * 100:.2f}%!")

if __name__ == "__main__":
    test_benchmark_quality()
