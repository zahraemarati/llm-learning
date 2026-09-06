from retrieval.vector_retriever import VectorRetriever
from retrieval.bm25_retriever import BM25Retriever



class HybridRetriever:


    def __init__(self):

        self.vector_retriever = VectorRetriever()

        self.bm25_retriever = BM25Retriever()



    def retrieve(
        self,
        query: str,
        n_results: int = 5
    ):


        semantic_results = (
            self.vector_retriever.retrieve(
                query,
                n_results=n_results
            )
        )


        keyword_results = (
            self.bm25_retriever.retrieve(
                query,
                k=n_results
            )
        )


        combined = {}



        # Semantic score weight
        for doc in semantic_results:

            text = doc["text"]

            combined[text] = {
                "text": text,
                "metadata": doc["metadata"],
                "score": (
                    0.7 *
                    doc["score"]
                )
            }



        # BM25 score weight
        for doc in keyword_results:

            text = doc["text"]


            bm25_score = doc["score"]


            if text in combined:

                combined[text]["score"] += (
                    0.3 *
                    bm25_score
                )


            else:

                combined[text] = {
                    "text": text,
                    "metadata": doc["metadata"],
                    "score": (
                        0.3 *
                        bm25_score
                    )
                }



        ranked_results = sorted(
            combined.values(),
            key=lambda x: x["score"],
            reverse=True
        )


        return ranked_results[:n_results]