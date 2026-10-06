from sentence_transformers import CrossEncoder


reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_documents(
    query: str,
    documents: list[dict],
    top_k: int = 3,
) -> list[dict]:
    if not documents:
        return []

    pairs = [
        [query, document["content"]]
        for document in documents
    ]

    scores = reranker_model.predict(pairs)

    ranked_documents = sorted(
        zip(documents, scores),
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        document
        for document, _ in ranked_documents[:top_k]
    ]