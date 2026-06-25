# ==========================================================
# IMPORTS
# ==========================================================

import os
import time
import json
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Import your LangGraph chatbot
from pipeline.rag_chatbot import graph


# ==========================================================
# FASTAPI
# ==========================================================

app = FastAPI(
    title="Local Agentic RAG",
    version="1.0"
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# STATIC FILES
# ==========================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ==========================================================
# LOGGING
# ==========================================================

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/rag_chatbot.log",
    level=logging.INFO,
    format="""
=====================================================
TIME: %(asctime)s
LEVEL: %(levelname)s

%(message)s
=====================================================
"""
)

logger = logging.getLogger(__name__)


# ==========================================================
# REQUEST MODEL
# ==========================================================

class ChatRequest(BaseModel):

    question: str

    thread_id: str = "default_user"


# ==========================================================
# HOME PAGE
# ==========================================================

@app.get("/")
async def home():

    return FileResponse(
        "static/index.html"
    )


# ==========================================================
# CHAT ENDPOINT
# ==========================================================

@app.post("/chat")
async def chat(request: ChatRequest):

    start_time = time.time()

    try:

        logger.info(
            f"USER QUESTION: {request.question}"
        )

        initial_state = {

            "user_query":
                request.question,

            "is_safe":
                True,

            "rephrased_user_query":
                "",

            "detected_intent":
                "",

            "retrieval_chunks":
                [],

            "response":
                "",

            "evaluation_score":
                0.0
        }

        # ==================================================
        # RUN LANGGRAPH
        # ==================================================

        result = graph.invoke(
            initial_state
        )

        answer = result.get("response")
        if isinstance(answer, dict):
            answer = answer.get("answer") or answer.get("response") or json.dumps(answer)
        if answer is None:
            answer = result.get("answer")
        if isinstance(answer, dict):
            answer = answer.get("answer") or answer.get("response") or json.dumps(answer)
        if answer is None:
            answer = "I could not find the answer in the knowledge base."
        else:
            answer = str(answer)

        latency = round(
            time.time() - start_time,
            2
        )

        score = result.get("evaluation_score")
        if isinstance(score, dict):
            score = score.get("score") or score.get("evaluation_score") or score.get("value")
        if score is None:
            score = result.get("score")
        if isinstance(score, dict):
            score = score.get("score") or score.get("evaluation_score") or score.get("value")
        if score is None:
            score = extract_score_from_result(result)

        try:
            score = float(score)
        except (TypeError, ValueError):
            score = 0.0

        logger.info(
            f"BOT RESPONSE: {answer}"
        )

        logger.info(
            f"LATENCY: {latency}"
        )

        logger.info(
            f"EVALUATION SCORE: {score}"
        )

        return {
            "question": request.question,
            "answer": answer,
            "response": answer,
            "score": score if score is not None else 0.0,
            "evaluation_score": score if score is not None else 0.0,
            "latency_seconds": latency
        }

    except Exception as e:

        logger.exception(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def extract_score_from_result(result):
    if not isinstance(result, dict):
        return None

    chunks = result.get("retrieval_chunks") or []
    if not isinstance(chunks, list):
        return None

    for chunk in chunks:
        if hasattr(chunk, "score"):
            return getattr(chunk, "score")
        if hasattr(chunk, "similarity_score"):
            return getattr(chunk, "similarity_score")
        if hasattr(chunk, "metadata") and isinstance(chunk.metadata, dict):
            for key in ["score", "similarity_score", "relevance_score"]:
                if chunk.metadata.get(key) is not None:
                    return chunk.metadata.get(key)
        if isinstance(chunk, dict):
            for key in ["score", "similarity_score", "relevance_score"]:
                if chunk.get(key) is not None:
                    return chunk.get(key)
    return None


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8111,
        reload=True
    )