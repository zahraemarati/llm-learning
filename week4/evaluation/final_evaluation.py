import csv

from evaluation.dataset import FINAL_EVALUATION_QUESTIONS

from rag_pipeline import retrieve_chunks

from context.context_manager import manage_context
from generation.answer_generator import generate_answer


OUTPUT_FILE = "evaluation/final_results.csv"



def ask_yes_no(message):

    while True:

        value = input(
            message
        ).strip().lower()


        if value in ["y", "yes"]:
            return "Yes"


        if value in ["n", "no"]:
            return "No"


        print(
            "Please enter y or n."
        )



def run_evaluation():

    results = []


    for index, question in enumerate(
        FINAL_EVALUATION_QUESTIONS,
        start=1
    ):

        print(
            "\n"
            + "=" * 70
        )

        print(
            f"QUESTION {index}/"
            f"{len(FINAL_EVALUATION_QUESTIONS)}"
        )

        print(
            question
        )


        retrieved_chunks = retrieve_chunks(
            question,
            candidate_count=10,
            top_k=5
        )


        print(
            "\nTOP RETRIEVED CHUNKS:"
        )


        for chunk_index, chunk in enumerate(
            retrieved_chunks,
            start=1
        ):

            print(
                f"\n--- Chunk {chunk_index} ---"
            )

            print(
                "Hybrid score:",
                chunk.get("score")
            )

            print(
                "Rerank score:",
                chunk.get("rerank_score")
            )

            print(
                chunk["text"][:500]
            )


        retrieved_correct = ask_yes_no(
            "\nRetrieved information correct? (y/n): "
        )


        context = manage_context(
            retrieved_chunks,
            max_chunks=5
        )


        answer = generate_answer(
            question,
            [context]
        )


        print(
            "\nGENERATED ANSWER:"
        )

        print(
            answer
        )


        answer_correct = ask_yes_no(
            "\nAnswer correct? (y/n): "
        )


        results.append(
            {
                "question": question,
                "retrieved_correct": retrieved_correct,
                "answer_correct": answer_correct,
                "answer": answer,
            }
        )


        save_results(
            results
        )


    print(
        "\nEvaluation completed."
    )

    print(
        f"Results saved to {OUTPUT_FILE}"
    )



def save_results(results):

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "question",
                "retrieved_correct",
                "answer_correct",
                "answer",
            ],
        )


        writer.writeheader()

        writer.writerows(
            results
        )



if __name__ == "__main__":
    run_evaluation()