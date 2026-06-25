from langchain_core.documents import Document

from chunking.chunker import recursive_chunker


def test_recursive_chunker():

    docs = [
        Document(
            page_content="LangGraph is a framework for stateful agents."
        )
    ]

    result = recursive_chunker(docs)

    assert len(result) > 0

    assert result[0].page_content is not None