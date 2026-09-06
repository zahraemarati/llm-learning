from retrieval.retriever import retrieve


question = "What is Artificial Intelligence?"


results = retrieve(
    question,
    n_results=10
)


for i, result in enumerate(results):

    print("\nRESULT:", i + 1)

    print("Text:")
    print(result["text"][:500])

    print("\nMetadata:")
    print(result["metadata"])

    print("\nDistance:")
    print(result["distance"])