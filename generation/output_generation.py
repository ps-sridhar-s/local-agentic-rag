from langchain_ollama import ChatOllama
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)

def rag_chat(user_query:str,retrived_chunks:list):
    response=llm.invoke(user_query)
    return response


def chit_chat(user_query:str):
    response=llm.invoke(user_query)
    return response