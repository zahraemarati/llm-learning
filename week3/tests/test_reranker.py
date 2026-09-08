from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker


retriever = HybridRetriever()
reranker = Reranker()



def test_reranker_returns_top_k():

    query = "What are the limitations of artificial intelligence?"


    candidates = retriever.retrieve(
        query,
        n_results=10
    )


    results = reranker.rerank(
        query,
        candidates,
        top_k=3
    )


    assert len(results) == 3



    for result in results:

        assert "text" in result
        assert "rerank_score" in result



def test_reranker_score_exists():

    query = "Explain machine learning"


    candidates = retriever.retrieve(
        query,
        n_results=10
    )


    results = reranker.rerank(
        query,
        candidates,
        top_k=5
    )


    scores = [
        r["rerank_score"]
        for r in results
    ]


    assert all(
        isinstance(score, float)
        for score in scores
    )