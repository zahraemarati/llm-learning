from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker

from evaluation.dataset import evaluation_questions
from evaluation.metrics import precision_at_k



retriever = HybridRetriever()

reranker = Reranker()



for item in evaluation_questions:


    question = item["question"]


    keywords = item["relevant_keywords"]


    print("\n================")
    print(question)



    results = retriever.retrieve(
        question,
        n_results=10
    )


    hybrid_score = precision_at_k(
        results,
        keywords,
        k=5
    )


    reranked = reranker.rerank(
        question,
        results,
        top_k=5
    )


    rerank_score = precision_at_k(
        reranked,
        keywords,
        k=5
    )


    print(
        "Hybrid Precision:",
        hybrid_score
    )


    print(
        "After Rerank:",
        rerank_score
    )