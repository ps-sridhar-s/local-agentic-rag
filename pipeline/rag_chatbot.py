from langgraph.graph import StateGraph,START,END
from typing import TypedDict
from generation.output_generation import chit_chat,rag_chat
from similarity_retrieval.vector_search_tool import vector_search

class Chat_State(TypedDict):
    user_query:str
    is_safe:bool
    rephrased_user_query:str
    detected_intent:str
    retrieval_chunks:list
    response:str
   




def user_query_node(state: Chat_State):

    user_query = state["user_query"]

    cleaned_query = user_query.strip()

    return {
        "rephrased_user_query": cleaned_query
    }



def guardrail_node(state):

    query = state["user_query"]

    banned_words = [
        "hack",
        "malware",
        "bomb"
    ]

    for word in banned_words:
        if word in query.lower():
            return {
                "is_safe": False,
                "response": "I cannot answer this query."
            }

    return {
        "is_safe": True
    }



def unsafe_node(state: Chat_State):

    return {
        "response": "I cannot answer this query."
    }

def intent_detection_node(state: Chat_State):

    query = state["rephrased_user_query"].lower()

    greetings = [
        "hi",
        "hello",
        "hey"
    ]

    if query in greetings:

        intent = "chitchat"

    else:

        intent = "rag"

    return {
        "detected_intent": intent
    }





def chit_chat_agent_node(state: Chat_State):
    response=chit_chat(state['rephrased_user_query'])

    return {
        "response": response
    }

def retrieval_query_node(state:Chat_State):
    retrieved_chunks=vector_search(user_query=state['user_query'],top_k=5)
    print(retrieved_chunks)
    return {"retrieval_chunks":retrieved_chunks}


    

def rag_agent_node(state):

    response = rag_chat(
        user_query=state['rephrased_user_query'],
        retrived_chunks=state['retrieval_chunks']
    )

    if hasattr(response, "content"):
        response = response.content

    return {
        "response": response
    }



def route_intent(state: Chat_State):

    intent = state["detected_intent"]

    if intent == "chitchat":
        return "chitchat"

    return "rag"




chat_graph=StateGraph(Chat_State)

chat_graph.add_node("user_query",user_query_node)
chat_graph.add_node(
    "guardrail",
    guardrail_node
)
chat_graph.add_node("intent_detection",intent_detection_node)

chat_graph.add_node("chit_chat_agent",chit_chat_agent_node)
chat_graph.add_node("retrieval_query",retrieval_query_node)
chat_graph.add_node("rag_agent",rag_agent_node)



chat_graph.add_edge(START,"user_query")
chat_graph.add_edge("user_query","intent_detection")
chat_graph.add_conditional_edges(
    "intent_detection",

    route_intent,

    {
        "chitchat": "chit_chat_agent",

        "rag": "retrieval_query"
    }
)

chat_graph.add_edge(
    "retrieval_query",
    "rag_agent"
)


chat_graph.add_edge(
    "chit_chat_agent",
    END
)


chat_graph.add_edge(
    "rag_agent",
    END
)


graph = chat_graph.compile()




if __name__ == "__main__":

    initial_state = {
        "user_query": "what is langchain?",
        "is_safe": True,
        "rephrased_user_query": "",
        "detected_intent": "",
        "retrieval_chunks": [],
        "response": ""
    }

    for event in graph.stream(
            initial_state,
            stream_mode="debug"
    ):

        print("\n========== EVENT ==========")
        print(event)