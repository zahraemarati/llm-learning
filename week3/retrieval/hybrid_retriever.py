from retrieval.retriever import retrieve
from retrieval.bm25_retriever import BM25Retriever


bm25 = BM25Retriever()


def hybrid_retrieve(
    query: str,
    n_results: int = 5
):

    semantic_results = retrieve(
        query,
        n_results=n_results
    )


    keyword_results = bm25.retrieve(
        query,
        k=n_results
    )


    merged = []

    seen = set()


    for item in (
        semantic_results +
        keyword_results
    ):

        text = item["text"]

        if text not in seen:

            merged.append(item)
            seen.add(text)


    return merged[:n_results]