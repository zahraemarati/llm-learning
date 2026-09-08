from retrieval.vector_retriever import retrieve
from generation.answer_generator import generate_answer


def ask_question(question: str):

    results = retrieve(
        question,
        n_results=5
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


    return answer, sources



if __name__ == "__main__":

    print("=== PDF Chat Assistant ===")


    while True:

        question = input("\nQuestion: ")


        if question.lower() == "exit":
            break


        answer, sources = ask_question(question)


        print("\nAnswer:")
        print(answer)


        print("\nSources:")

        for source in sources:
            print(
                f"- {source['source']} | Page {source['page']}"
            )