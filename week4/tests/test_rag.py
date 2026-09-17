from rag_pipeline import ask_question


def test_rag_pipeline():

    question = (
        "What are the major development "
        "trends of intelligent technologies?"
    )

    result = ask_question(
        question
    )


    assert result is not None

    assert "answer" in result

    assert "sources" in result

    assert len(result["answer"]) > 0

    assert len(result["sources"]) > 0