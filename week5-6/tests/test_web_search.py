from tools.web_search import web_search


def test_web_search():
    result = web_search.invoke(
        {
            "query": "Python programming language",
        }
    )

    assert isinstance(result, str)
    assert len(result) > 0