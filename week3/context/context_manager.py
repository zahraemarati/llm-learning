def manage_context(
    retrieved_chunks,
    max_chunks=5
):

    selected_chunks = retrieved_chunks[:max_chunks]


    context = "\n\n".join(
        chunk["text"]
        for chunk in selected_chunks
    )


    return context