import random
import json
from sklearn.metrics import classification_report
import requests

# Função para gerar dados sintéticos
def generate_synthetic_data(num_samples):
    # Lista expandida de palavras positivas e negativas
    positive_words_en = ["happy", "great", "amazing", "fantastic", "love", "joyful", "excited", "delighted", "thrilled", "awesome"]
    negative_words_en = ["sad", "terrible", "awful", "hate", "bad", "disappointed", "frustrated", "horrible", "miserable", "angry"]
    positive_words_pt = ["feliz", "ótimo", "incrível", "fantástico", "amor", "alegre", "empolgado", "encantado", "radiante", "maravilhoso"]
    negative_words_pt = ["triste", "terrível", "horrível", "ódio", "ruim", "decepcionado", "frustrado", "pavoroso", "miserável", "irritado", "desastroso", "atroz", "decepcionante", "insuportável"]
    
    # Palavras para adicionar intensidade
    intensity_words_en = ["really", "so", "extremely", "super", "incredibly", "absolutely", "totally"]
    intensity_words_pt = ["realmente", "muito", "extremamente", "super", "incrivelmente", "absolutamente", "totalmente"]

    synthetic_data = []
    
    for _ in range(num_samples):
        sentiment = random.choice(["POSITIVE", "NEGATIVE"])
        language = random.choice(["EN", "PT"])
        
        # Adicionar palavras de intensidade nas frases
        if sentiment == "POSITIVE":
            if language == "EN":
                intensity = random.choice(intensity_words_en)
                text = f"I am {intensity} feeling {random.choice(positive_words_en)} today."
            else:
                intensity = random.choice(intensity_words_pt)
                text = f"Estou {intensity} me sentindo {random.choice(positive_words_pt)} hoje."
        else:
            if language == "EN":
                intensity = random.choice(intensity_words_en)
                text = f"I am {intensity} feeling {random.choice(negative_words_en)} today."
            else:
                intensity = random.choice(intensity_words_pt)
                text = f"Estou {intensity} me sentindo {random.choice(negative_words_pt)} hoje."
        
        synthetic_data.append({"text": text, "expected": sentiment})
    
    return synthetic_data

def test_benchmark_quality():
    # Gerar dados sintéticos
    synthetic_data = generate_synthetic_data(100)  # Gerar 45 amostras sintéticas
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
    report = classification_report(
        true_labels, predicted_labels, output_dict=True, zero_division=1, labels=["POSITIVE", "NEGATIVE", "NEUTRAL"]
    )

    # Exibir resultados
    print("\nBenchmarking de Qualidade de Inferência:")
    print(f"Precisão: {report['accuracy'] * 100:.2f}%")
    for label in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
        print(f"Recall ({label}): {report[label]['recall'] * 100:.2f}%")
        print(f"F1 Score ({label}): {report[label]['f1-score'] * 100:.2f}%")

    # Critérios de aceitação
    MIN_ACCURACY = 0.8
    assert report["accuracy"] >= MIN_ACCURACY, f"A precisão do modelo está abaixo do limite aceitável de {MIN_ACCURACY * 100:.2f}%!"

if __name__ == "__main__":
    test_benchmark_quality()

