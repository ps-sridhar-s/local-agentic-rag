from langchain_text_splitters import (
    TokenTextSplitter
)

from langchain_core.documents import Document


def token_chunker(
        documents: list[Document]
) -> list[Document]:

    """
    Split documents based on token count.
    """

    if not documents:
        return []

    splitter = TokenTextSplitter(
        chunk_size=512,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(
        documents
    )

    return chunks