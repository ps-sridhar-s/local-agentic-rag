
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from langchain.embeddings import OllamaEmbeddings
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from document_loader.file_loader import data_loader,clean_documents
from chunking.chunker import recursive_chunker
from models.embedding_models import embed_model
from embedding.generate_embeddings import embed_query
# from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
import os

from uuid import uuid4

embeddings = OllamaEmbeddings(
    model="mxbai-embed-large"
)
class Rag_State(TypedDict):
    files:list
    docs:list
    chunks:list
    retrieved_chunks: list

def knowledge_source_node(state:Rag_State):

    folder_path = "data_source"

    files = []

    for file in os.listdir(folder_path):

        full_path = os.path.join(
            folder_path,
            file
        )

        if os.path.isfile(full_path):
            files.append(full_path)

    return {"files":files}





def document_loading_node(state:Rag_State):
    files=state['files']
    all_documents=[]
    for file in files:
        docs=data_loader(file_path=file)
        cleaned_docs = clean_documents(docs)
        all_documents.extend(cleaned_docs)
    return {
        "docs": all_documents
    }
        
    


def chunking_node(state:Rag_State):
    documents=state['docs']
    splited_content=recursive_chunker(documents)
    return {
        "chunks": splited_content
    }





def embedding_node(state:Rag_State):
    chunks=state['chunks']
    embedd_chunk=[]
    for chunk in chunks:
        embedd_chunk.extend(embed_query(chunk.page_content))
    return {
        "embeddings": embedd_chunk
    }








def indexing_node(state):

    chunks = state["chunks"]

    db = FAISS.from_documents(
        documents=chunks,
        embedding=embed_model
    )

    db.save_local(
        "./data_warehouse/faiss_index"
    )

    print(
        f"Indexed {len(chunks)} chunks into FAISS"
    )

    return state

builder=StateGraph(Rag_State)
builder.add_node(
    "knowledge_source",
    knowledge_source_node
)
builder.add_node("document_loading",document_loading_node)
builder.add_node("chunking", chunking_node)
# builder.add_node("embedding",embedding_node)
builder.add_node("indexing",indexing_node)



builder.add_edge(
    START,
    "knowledge_source"
)
builder.add_edge(
    "knowledge_source",
    "document_loading"
)

builder.add_edge(
    "document_loading",
    "chunking"
)


builder.add_edge(
    "chunking",
    "indexing"
)


builder.add_edge(
    "indexing",
    END
)

graph = builder.compile()



if __name__ == "__main__":

    # result = graph.invoke(
    initial_state=    {
            "files": [],
            "docs": [],
            "chunks": [],
            "retrieved_chunks": []
        }
    # )

    for event in graph.stream(
            initial_state,
            stream_mode="debug"
    ):

        print("\n========== EVENT ==========")
        print(event)
    print("Process Done")

    # print(result)




