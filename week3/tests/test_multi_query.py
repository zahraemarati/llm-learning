from query.multi_query import MultiQueryGenerator



def test_multi_query():

    generator = MultiQueryGenerator()


    queries = generator.generate(
        "How does AI learn?"
    )


    assert isinstance(queries, list)
    assert len(queries) == 3