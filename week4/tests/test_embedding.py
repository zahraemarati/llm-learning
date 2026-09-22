from embeddings.embedder import get_embedding


def test_embedding():

    text = "Artificial intelligence is changing technology."

    vector = get_embedding(text)

    assert vector

    assert isinstance(vector, list)

    assert len(vector) > 0