from rank_bm25 import BM25Okapi
import chromadb

from config import settings


client = chromadb.PersistentClient(
    path=settings.chroma_path
)


def get_all_documents():

    collection = client.get_collection(
        name=settings.collection_name
    )

    results = collection.get()

    documents = results["documents"]
    metadatas = results["metadatas"]

    return [
        {
            "text": doc,
            "metadata": metadata,
        }
        for doc, metadata in zip(
            documents,
            metadatas,
        )
    ]


class BM25Retriever:

    def __init__(self):

        self.documents = get_all_documents()

        tokenized_docs = [
            doc["text"].split()
            for doc in self.documents
        ]

        self.bm25 = BM25Okapi(
            tokenized_docs
        )


    def retrieve(
        self,
        query: str,
        k: int = 5
    ):

        tokenized_query = query.split()

        scores = self.bm25.get_scores(
            tokenized_query
        )


        ranked = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )


        results = []

        for index in ranked[:k]:

            results.append(
                {
                    "text": self.documents[index]["text"],
                    "metadata": self.documents[index]["metadata"],
                    "score": scores[index],
                }
            )


        return results