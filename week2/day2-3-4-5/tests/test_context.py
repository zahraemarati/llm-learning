# from retrieval.retriever import retrieve
# from context.context_manager import manage_context


# question = "What is Artificial Intelligence?"


# results = retrieve(
#     question,
#     n_results=10
# )


# context = manage_context(
#     results,
#     max_chunks=5
# )


# print(context)

from retrieval.retriever import retrieve
from context.context_manager import manage_context


question = "What is Artificial Intelligence?"


results = retrieve(
    question,
    n_results=10
)


print("Retrieved results:", len(results))


for i, item in enumerate(results):
    print("\nRESULT", i+1)
    print("Distance:", item["distance"])
    print("Metadata:", item["metadata"])
    print(item["text"][:200])


context = manage_context(
    results,
    max_chunks=5
)


print("\n\nFINAL CONTEXT:")
print(context)