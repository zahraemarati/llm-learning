from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from retrieval.vector_retriever import VectorRetriever


class LangChainVectorRetriever(BaseRetriever):
    k: int = 5

    def _get_relevant_documents(
        self,
        query: str,
    ) -> list[Document]:

        vector_retriever = VectorRetriever()

        results = vector_retriever.retrieve(
            query,
            n_results=self.k,
        )

        documents = []

        for result in results:

            metadata = result.get(
                "metadata",
                {}
            ).copy()

            metadata["score"] = result.get(
                "score"
            )

            document = Document(
                page_content=result["text"],
                metadata=metadata,
            )

            documents.append(document)

        return documents