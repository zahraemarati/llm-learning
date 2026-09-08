from query.query_rewriter import QueryRewriter


def test_query_rewrite():

    rewriter = QueryRewriter()

    result = rewriter.rewrite(
        "How does AI learn?"
    )

    assert isinstance(result, str)
    assert len(result) > 0