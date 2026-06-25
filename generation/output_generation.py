# generation/output_generation.py

import json

from langchain_ollama import ChatOllama

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)

# ==========================================================
# LLM INITIALIZATION
# ==========================================================

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)

parser = StrOutputParser()

# ==========================================================
# RAG PROMPT TEMPLATE
# ==========================================================

rag_prompt = ChatPromptTemplate.from_messages(

    [

        (

            "system",

            """
You are an expert AI assistant specialized in:

- LangChain
- LangGraph
- Retrieval-Augmented Generation (RAG)
- Generative AI
- Large Language Models

You MUST answer ONLY using the provided context.

Instructions:

1. Use only the supplied context.
2. Do not hallucinate.
3. If the answer is unavailable in the context, respond exactly:

"I could not find the answer in the knowledge base."
4. Return only valid JSON with exactly two keys: "answer" and "score".
5. "answer" should contain the response text.
6. "score" should contain a confidence value between 0.0 and 1.0.
7. Do not include any text outside the JSON object.

Example:

{{"answer": "The top result is ...", "score": 0.78}}

Context:
{context}
            """

        ),

        (

            "human",

            """
Question:
{question}
            """

        )

    ]

)

# ==========================================================
# CHITCHAT PROMPT TEMPLATE
# ==========================================================

chitchat_prompt = ChatPromptTemplate.from_messages(

    [

        (

            "system",

            """
You are a friendly conversational AI assistant.

Your responsibilities:

- Greetings
- Casual conversation
- General assistance

Rules:

- Be friendly and professional.
- Keep answers short and conversational.
- If the user asks highly technical LangChain or RAG questions,
  politely answer if possible.
- Return only valid JSON with exactly two keys: "answer" and "score".
- "answer" should contain the response text.
- "score" should contain a confidence value between 0.0 and 1.0.
- Do not include any text outside the JSON object.

Examples:

User: Hi
Assistant: {{"answer": "Hello! How can I assist you today?", "score": 0.9}}

User: How are you?
Assistant: {{"answer": "I'm doing great. How can I help you?", "score": 0.9}}

User: Thank you
Assistant: {{"answer": "You're welcome! Happy to help.", "score": 0.9}}
            """

        ),

        (

            "human",

            "{question}"

        )

    ]

)

# ==========================================================
# LCEL CHAINS
# ==========================================================

rag_chain = (

        rag_prompt

        | llm

        | parser

)

chitchat_chain = (

        chitchat_prompt

        | llm

        | parser

)

# ==========================================================
# RAG AGENT
# ==========================================================

def parse_json_response(response_text: str):
    if not isinstance(response_text, str):
        return None

    trimmed = response_text.strip()
    candidates = [trimmed]
    if trimmed.startswith("'") and trimmed.endswith("'"):
        candidates.append(trimmed.replace("'", '"'))
    if trimmed.startswith('"') and trimmed.endswith('"'):
        candidates.append(trimmed.replace('""', '"'))

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict) and "answer" in parsed and "score" in parsed:
                return {
                    "answer": str(parsed.get("answer", "")),
                    "score": float(parsed.get("score", 0.0))
                }
        except (json.JSONDecodeError, TypeError, ValueError):
            continue

    # Try to find a JSON object inside the text
    try:
        start = trimmed.index("{")
        end = trimmed.rindex("}")
        inner = trimmed[start:end+1]
        parsed = json.loads(inner)
        if isinstance(parsed, dict) and "answer" in parsed and "score" in parsed:
            return {
                "answer": str(parsed.get("answer", "")),
                "score": float(parsed.get("score", 0.0))
            }
    except (ValueError, json.JSONDecodeError, TypeError):
        pass

    return None


def rag_chat(
        user_query: str,
        retrieved_chunks: list
):
    if not retrieved_chunks:
        return {
            "answer": "I could not find the answer in the knowledge base.",
            "score": 0.0
        }

    context = "\n\n".join(
        [chunk.page_content for chunk in retrieved_chunks]
    )

    print("\n========== RAG CONTEXT ==========\n")
    print(context[:1000])
    print("\n=================================\n")

    response_text = rag_chain.invoke(
        {
            "question": user_query,
            "context": context
        }
    )

    parsed = parse_json_response(response_text)
    if parsed is not None:
        return parsed

    return {
        "answer": response_text,
        "score": 0.0
    }


# ==========================================================
# CHITCHAT AGENT
# ==========================================================

def chit_chat(
        user_query: str
):
    response_text = chitchat_chain.invoke(
        {
            "question": user_query
        }
    )

    parsed = parse_json_response(response_text)
    if parsed is not None:
        return parsed

    return {
        "answer": response_text,
        "score": 0.0
    }



