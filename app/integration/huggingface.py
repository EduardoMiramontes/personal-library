import requests
import os

class HuggingFaceClassifier:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
        self.headers = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}
        self.etiquetas = [
            "Ciencia ficción", "Fantasía", "Romance", "Terror", "Misterio",
            "Drama", "Aventura", "Comedia", "Thriller", "Distopía",
            "Historia", "Política", "Filosofía", "Psicología", "Sociología",
            "Economía", "Religión", "Ciencias naturales", "Ciencias sociales",
            "Educación", "Arte", "Música", "Matemáticas", "Tecnología", "Ecología",
            "Poesía", "Ensayo", "Biografía", "Autobiografía", "Crónica", "Epistolar",
            "Teatro", "Cuento", "Novela gráfica", "Literatura infantil", "Literatura juvenil",
            "Literatura mexicana", "Literatura latinoamericana", "Literatura española",
            "Literatura estadounidense", "Literatura africana", "Literatura asiática",
            "Literatura europea", "Literatura indígena", "Ficción histórica",
            "Ficción especulativa", "Realismo mágico", "No ficción", "Autoficción",
            "Periodismo narrativo", "Género y feminismo", "Diversidad sexual",
            "Racismo y discriminación", "Derechos humanos", "Migración", "Violencia",
            "Memoria histórica", "Espiritualidad", "Mitología", "Esoterismo",
            "Nueva era", "Viajes", "Humor", "Autoayuda", "Desarrollo personal",
            "Cultura popular"
        ]

    def clasificar(self, texto, etiquetas_personalizadas=None):
        payload = {
            "inputs": texto,
            "parameters": {
                "candidate_labels": etiquetas_personalizadas or self.etiquetas
            }
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code != 200:
            print("Error con la API de Hugging Face:", response.text)
            return None

        try:
            data = response.json()
            return list(zip(data["labels"], data["scores"]))
        except Exception as e:
            print("Error al procesar respuesta:", e)
            return None