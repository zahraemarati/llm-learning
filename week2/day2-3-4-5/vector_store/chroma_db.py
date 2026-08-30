import chromadb

from embeddings.embedder import get_embedding
from document_loader.pdf_loader import load_pdf
from document_loader.splitter.chunker import get_chunks


client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="pdf_documents"
)


def create_vector_store(pdf_path: str):

    documents = load_pdf(pdf_path)

    chunks = get_chunks(documents)


    for index, chunk in enumerate(chunks):

        text = chunk.page_content

        embedding = get_embedding(text)


        collection.add(
            ids=[
                f"chunk_{index}"
            ],

            documents=[
                text
            ],

            embeddings=[
                embedding
            ],

            metadatas=[
                chunk.metadata
            ]
        )


    return {
        "message": "PDF processed successfully",
        "chunks": len(chunks)
    }