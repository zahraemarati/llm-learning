from pathlib import Path

import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from config import settings
from llm_client import embedding_client


def load_pdf(file_path: str) -> list[dict]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    reader = PdfReader(path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if not text:
            continue

        pages.append(
            {
                "content": text,
                "metadata": {
                    "source": path.name,
                    "page": page_number,
                },
            }
        )

    return pages


def chunk_pages(pages: list[dict]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )

    chunks = []

    for page in pages:
        texts = splitter.split_text(page["content"])

        for chunk_index, text in enumerate(texts):
            chunks.append(
                {
                    "content": text,
                    "metadata": {
                        **page["metadata"],
                        "chunk": chunk_index,
                    },
                }
            )

    return chunks


def embed_texts(
    texts: list[str],
    batch_size: int = 128,
) -> list[list[float]]:
    embeddings = []

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]

        response = embedding_client.embeddings.create(
            model=settings.embed_model,
            input=batch,
        )

        embeddings.extend(
            item.embedding
            for item in response.data
        )

    return embeddings


def ingest_pdf(file_path: str) -> int:
    pages = load_pdf(file_path)
    chunks = chunk_pages(pages)

    if not chunks:
        return 0

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = embed_texts(texts)

    client = chromadb.PersistentClient(
        path=settings.chroma_path,
    )

    collection = client.get_or_create_collection(
        name=settings.collection_name,
    )

    path = Path(file_path)

    ids = [
        f"{path.stem}-p{chunk['metadata']['page']}-c{chunk['metadata']['chunk']}"
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=[
            chunk["metadata"]
            for chunk in chunks
        ],
    )

    return len(chunks)