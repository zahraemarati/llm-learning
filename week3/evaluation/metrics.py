def precision_at_k(
    results,
    keywords,
    k
):

    results = results[:k]


    relevant = 0


    for result in results:

        text = result["text"].lower()


        if any(
            keyword.lower()
            in text
            for keyword in keywords
        ):
            relevant += 1


    return relevant / k