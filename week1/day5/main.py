with open("knowledge.txt", "r") as f:
    text = f.read()

print(text)

# chunks
chunks = text.split("\n")

print(chunks)