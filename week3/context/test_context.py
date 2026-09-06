from retrieval.vector_retriever import retrieve
from context.context_manager import manage_context


question = "What is Artificial Intelligence?"


results = retrieve(
    question,
    n_results=10
)


context = manage_context(
    results,
    max_chunks=5
)


print(context)