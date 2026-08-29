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


print("\nMetadata:")
print(chunks[0].metadata)

print("Total chunks:", len(chunks))

for i in range(20, 25):
    print(f"\nChunk {i}")
    print("Length:", len(chunks[i].page_content))
    print("Metadata:", chunks[i].metadata)
    print(chunks[i].page_content)
    print("-" * 50)

