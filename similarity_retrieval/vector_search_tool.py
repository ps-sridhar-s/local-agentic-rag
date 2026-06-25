# similarity_retrieval/vector_search.py

from langchain_community.vectorstores import FAISS
from models.embedding_models import embed_model


# ==========================================================
# LOAD FAISS VECTOR DATABASE
# ==========================================================

def load_vector_db():
    """
    Loads the persisted FAISS vector database.
    """

    db = FAISS.load_local(
        folder_path="./data_warehouse/faiss_index",
        embeddings=embed_model,
        allow_dangerous_deserialization=True
    )

    return db


# ==========================================================
# VECTOR SEARCH
# ==========================================================

def vector_search(
        user_query: str,
        top_k: int = 5
):
    """
    Searches the FAISS vector database
    using similarity search.
    """

    db = load_vector_db()

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": top_k
        }
    )

    retrieved_docs = retriever.invoke(
        user_query
    )

    return retrieved_docs


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    docs = vector_search(
        user_query="What is Python?",
        top_k=5
    )

    print(
        f"Retrieved {len(docs)} documents\n"
    )

    for idx, doc in enumerate(docs, start=1):

        print("=" * 80)
        print(f"Document {idx}")
        print("=" * 80)

        print(doc.page_content)
        print("\nMetadata:")
        print(doc.metadata)
        print()