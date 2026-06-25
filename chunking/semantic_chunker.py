from langchain_experimental.text_splitter import (
    SemanticChunker
)

from langchain_ollama import (
    OllamaEmbeddings
)

from langchain_core.documents import Document


def semantic_chunker(documents):

    embeddings = OllamaEmbeddings(
        model="mxbai-embed-large"
    )

    splitter = SemanticChunker(
        embeddings=embeddings
    )

    chunks = splitter.split_documents(
        documents
    )

    return chunks