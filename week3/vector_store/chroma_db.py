import os

import chromadb

from embeddings.embedder import get_embeddings
from document_loader.pdf_loader import load_pdf
from document_loader.splitter.chunker import get_chunks


CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "pdf_documents"
EMBEDDING_BATCH_SIZE = 50


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def create_vector_store(pdf_path: str):
    documents = load_pdf(pdf_path)
    chunks = get_chunks(documents)

    filename = os.path.basename(pdf_path)

    # If the same PDF is ingested again, remove its old chunks first.
    collection.delete(
        where={
            "source": filename
        }
    )

    for start in range(
        0,
        len(chunks),
        EMBEDDING_BATCH_SIZE,
    ):
        batch = chunks[
            start:start + EMBEDDING_BATCH_SIZE
        ]

        texts = [
            chunk.page_content
            for chunk in batch
        ]

        embeddings = get_embeddings(texts)

        ids = []
        metadatas = []

        for offset, chunk in enumerate(batch):
            index = start + offset

            # PyPDFLoader uses zero-based page indexes.
            # The project stores page numbers as one-based values:
            # page 1 in the PDF => metadata["page"] == 1.
            page_number = int(
                chunk.metadata.get("page", 0)
            ) + 1

            ids.append(
                f"{filename}_chunk_{index}"
            )

            metadatas.append(
                {
                    "page": page_number,
                    "source": filename,
                }
            )

        collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    return {
        "message": "PDF processed successfully",
        "chunks": len(chunks),
    }
