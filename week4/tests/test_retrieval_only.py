import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from embeddings.embedder import get_embedding
from vector_store.chroma_db import collection


questions = [
    "What is artificial intelligence?",
    "What are the limitations of AI?",
    "Explain machine learning",
]


for question in questions:

    print("\n====================")
    print("QUESTION:")
    print(question)


    query_embedding = get_embedding(question)


    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=5
    )


    print("\nRetrieved chunks:")


    for i in range(len(results["documents"][0])):

        print("\n--- Result", i+1, "---")

        print(
            "Distance:",
            results["distances"][0][i]
        )

        print(
            "Metadata:",
            results["metadatas"][0][i]
        )

        print(
            results["documents"][0][i][:300]
        )