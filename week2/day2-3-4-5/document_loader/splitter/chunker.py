from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Load PDF
loader = PyPDFLoader("paper.pdf")

documents = loader.load()


print("Original documents:", len(documents))


# Create splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


# Split documents
chunks = text_splitter.split_documents(documents)

chunks = [
    chunk
    for chunk in chunks
    if chunk.metadata["page"] > 5
]

def get_chunks():
    return chunks

print("Chunks:", len(chunks))


print("\nFirst chunk:")
print(chunks[0].page_content)


print("\nMetadata:")
print(chunks[0].metadata)

