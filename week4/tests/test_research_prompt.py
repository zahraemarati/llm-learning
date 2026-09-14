from prompts.research_prompt import research_prompt


def test_research_prompt():
    result = research_prompt.invoke(
        {
            "question": "Explain Hybrid Retrieval"
        }
    )

    assert len(result.messages) == 2
    assert "Hybrid Retrieval" in result.messages[1].content