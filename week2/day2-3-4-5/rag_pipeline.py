from retrieval.retriever import retrieve
from context.context_manager import manage_context
from generation.answer_generator import generate_answer


def ask_question(question: str):

    retrieved_chunks = retrieve(
        question,
        n_results=10
    )


    context = manage_context(
        retrieved_chunks,
        max_chunks=5
    )


    answer = generate_answer(
        question,
        [context]
    )


    return answer