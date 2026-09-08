from sentence_transformers import CrossEncoder



class Reranker:


    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )



    def rerank(
        self,
        query,
        documents,
        top_k=5
    ):


        pairs = [
            (
                query,
                doc["text"]
            )
            for doc in documents
        ]


        scores = self.model.predict(
            pairs
        )


        reranked_documents = []


        for doc, score in zip(
            documents,
            scores
        ):

            new_doc = doc.copy()

            new_doc["rerank_score"] = float(
                score
            )

            reranked_documents.append(
                new_doc
            )



        reranked_documents.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )


        return reranked_documents[:top_k]