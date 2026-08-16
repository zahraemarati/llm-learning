import requests
import numpy as np


def get_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    return response.json()["embedding"]


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) *
        np.linalg.norm(b)
    )


texts = [
    "Python programming and software development",
    "Artificial intelligence and machine learning",
    "I like eating pizza on weekends"
]


embeddings = [
    get_embedding(text)
    for text in texts
]


print(
    "1 vs 2:",
    cosine_similarity(
        embeddings[0],
        embeddings[1]
    )
)


print(
    "1 vs 3:",
    cosine_similarity(
        embeddings[0],
        embeddings[2]
    )
)