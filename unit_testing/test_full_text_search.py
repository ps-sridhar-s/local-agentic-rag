from langchain_core.documents import Document
from similarity_retrieval.full_text_search import bm25_full_text_search

documents = [
    Document(
        page_content="LangGraph is a framework for building stateful AI agents.",
        metadata={"source": "langgraph"}
    ),

    Document(
        page_content="LangChain helps developers build LLM applications.",
        metadata={"source": "langchain"}
    ),

    Document(
        page_content="Python is a high-level programming language.",
        metadata={"source": "python"}
    )
]




def bm25_testing():
    searched_context=bm25_full_text_search(user_query="Hi",documents=documents,top_k=5)

