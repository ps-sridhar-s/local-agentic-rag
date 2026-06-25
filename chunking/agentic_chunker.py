from langchain_core.documents import Document
from models.chat_models import chat_llm
import json


def agentic_chunker(text):

    prompt = f"""
    Divide the document into
    concept-based chunks.

    Return JSON:

    [
      {{
        "title":"",
        "content":""
      }}
    ]

    Document:
    {text}
    """

    response = chat_llm.invoke(prompt)

    chunks = json.loads(
        response.content
    )

    docs = []

    for chunk in chunks:

        docs.append(

            Document(
                page_content=chunk["content"],
                metadata={
                    "title":
                    chunk["title"]
                }
            )
        )

    return docs