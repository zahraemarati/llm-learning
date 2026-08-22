from embeddings.embedder import get_embedding


text = "Python is a programming language"


vector = get_embedding(text)


print("Vector size:", len(vector))
print(vector[:5])