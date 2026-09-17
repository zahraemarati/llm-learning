from chains.summarizer_chain import summarizer_chain


def test_summarizer_chain():

    result = summarizer_chain.invoke(
        {
            "paper": """
            This paper studies artificial intelligence.
            The main result is improved performance.
            """
        }
    )


    assert result

    assert len(result) > 0