from retrieval.retriever import retrieve
from generation.answer_generator import generate_answer


question = "Define Artificial Intelligence and explain its meaning"


results = retrieve(
    question,
    n_results=10
)


contexts = [
    result["text"]
    for result in results
]


answer = generate_answer(
    question,
    contexts
)


sources = [
    result["metadata"]
    for result in results
]


print("\nAnswer:")
print(answer)


print("\nSources:")

for source in sources:
    print(
        f"- {source['source']} | Page {source['page']}"
    )