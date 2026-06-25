from rank_bm25 import BM25Okapi
from langchain_core.documents import Document


def bm25_full_text_search(
        user_query: str,
        documents: list[Document],
        top_k: int = 5
) -> list[Document]:

    # Convert documents to tokens

    tokenized_docs = [

        doc.page_content.lower().split()

        for doc in documents
    ]

    # Create BM25 index

    bm25 = BM25Okapi(tokenized_docs)

    # Tokenize query

    tokenized_query = user_query.lower().split()

    # Get scores

    scores = bm25.get_scores(tokenized_query)

    # Sort documents by score

    scored_docs = list(zip(documents, scores))

    ranked_docs = sorted(
        scored_docs,
        key=lambda x: x[1],
        reverse=True
    )

    # Return top-k docs

    top_documents = [

        doc

        for doc, score in ranked_docs[:top_k]
    ]

    return top_documents