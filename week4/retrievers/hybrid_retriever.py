from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from pydantic import PrivateAttr

from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker


class LangChainHybridRetriever(BaseRetriever):
    candidate_k: int = 10
    top_k: int = 5

    _hybrid_retriever: HybridRetriever = PrivateAttr()
    _reranker: Reranker = PrivateAttr()

    def model_post_init(self, __context):
        self._hybrid_retriever = HybridRetriever()
        self._reranker = Reranker()

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> list[Document]:

        # Step 1: Hybrid retrieval
        candidates = self._hybrid_retriever.retrieve(
            query,
            n_results=self.candidate_k,
        )

        # Step 2: Reranking
        reranked_results = self._reranker.rerank(
            query=query,
            documents=candidates,
            top_k=self.top_k,
        )

        # Step 3: Convert to LangChain Documents
        documents = []

        for result in reranked_results:

            metadata = result.get("metadata", {}).copy()

            metadata["hybrid_score"] = float(
                result.get("score", 0)
            )

            metadata["rerank_score"] = float(
                result.get("rerank_score", 0)
            )

            documents.append(
                Document(
                    page_content=result["text"],
                    metadata=metadata,
                )
            )

        return documents