import chromadb
from embeddings.embedder import get_embedding
from document_loader.splitter.chunker import get_chunks

client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="pdf_documents"
)


def create_vector_store():

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


    print(
        f"{len(chunks)} chunks stored successfully"
    )

chunks = get_chunks()

for index, chunk in enumerate(chunks):

    print(f"Processing {index+1}/{len(chunks)}")

    text = chunk.page_content

if __name__ == "__main__":
    create_vector_store()