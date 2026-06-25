from langchain_core.messages import AIMessage
from generation.output_generation import chit_chat,rag_chat


def test_chat():
    response = chit_chat("Hi")

    assert response is not None
    assert isinstance(response, AIMessage)
    assert len(response.content) > 0


def test_rag_chat():
    response = rag_chat("Hi","hello friend")
    assert response is not None
    assert isinstance(response, AIMessage)
    assert len(response.content) > 0

