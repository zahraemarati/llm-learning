from rank_bm25 import BM25Okapi
import chromadb

from config import settings

class BM25Retriever:


    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=settings.chroma_path
        )


        self.collection = self.client.get_collection(
            name=settings.collection_name
        )


        self.documents = self._load_documents()


        tokenized_docs = [
            doc["text"].split()
            for doc in self.documents
        ]


        self.bm25 = BM25Okapi(
            tokenized_docs
        )


    def _load_documents(self):

        results = self.collection.get()


        return [
            {
                "text": doc,
                "metadata": metadata
            }
            for doc, metadata in zip(
                results["documents"],
                results["metadatas"]
            )
        ]



    def retrieve(
        self,
        query: str,
        k: int = 5
    ):

        scores = self.bm25.get_scores(
            query.split()
        )


        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )


        results = []


        for index in ranked_indexes[:k]:

            results.append(
                {
                    "text": self.documents[index]["text"],
                    "metadata": self.documents[index]["metadata"],
                    "score": scores[index]
                }
            )


        return results