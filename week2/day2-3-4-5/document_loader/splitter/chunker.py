from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_chunks(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(
        documents
    )
    print("Chunks before filter:", len(chunks))

    chunks = [
        chunk
        for chunk in chunks
        if chunk.metadata["page"] >= 0
    ]
    print("Chunks after filter:", len(chunks))

    return chunks