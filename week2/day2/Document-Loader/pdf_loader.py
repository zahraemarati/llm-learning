from langchain_community.document_loaders import PyPDFLoader


loader = PyPDFLoader("../paper.pdf")


documents = loader.load()


print("Number of documents:", len(documents))


print("\nFirst page text:")
print(documents[0].page_content)


print("\nMetadata:")
print(documents[0].metadata)

print(type(documents))
print(type(documents[0]))



