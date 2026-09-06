from retrieval.vector_retriever import retrieve


QUESTION = "What is Artificial Intelligence?"


def test_search_entire_pdf():
    results = retrieve(
        QUESTION,
        n_results=10,
    )

    assert len(results) > 0


def test_search_from_page_10():
    results = retrieve(
        QUESTION,
        n_results=10,
        where={
            "page": {
                "$gte": 10
            }
        },
    )

    assert len(results) > 0

    assert all(
        result["metadata"]["page"] >= 10
        for result in results
    )


def test_search_between_pages_10_and_20():
    results = retrieve(
        QUESTION,
        n_results=10,
        where={
            "$and": [
                {
                    "page": {
                        "$gte": 10
                    }
                },
                {
                    "page": {
                        "$lte": 20
                    }
                },
            ]
        },
    )

    assert len(results) > 0

    assert all(
        10 <= result["metadata"]["page"] <= 20
        for result in results
    )
