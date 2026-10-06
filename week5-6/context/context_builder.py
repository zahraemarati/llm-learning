from typing import List, Dict


def build_context(
    documents: List[Dict],
) -> str:
    """
    Convert retrieved documents into LLM context.
    """

    contexts = []

    for index, document in enumerate(documents, start=1):
        contexts.append(
            f"Document {index}:\n"
            f"{document['content']}"
        )

    return "\n\n".join(contexts)