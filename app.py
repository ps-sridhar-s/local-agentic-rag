# ==========================================================
# IMPORTS
# ==========================================================

import os
import time
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
                ""
        }

        # ==================================================
        # RUN LANGGRAPH
        # ==================================================

        result = graph.invoke(
            initial_state
        )

        answer = result["response"]

        latency = round(
            time.time() - start_time,
            2
        )

        logger.info(
            f"BOT RESPONSE: {answer}"
        )

        logger.info(
            f"LATENCY: {latency}"
        )

        return {

            "question":
                request.question,

            "answer":
                answer,

            "latency_seconds":
                latency
        }

    except Exception as e:

        logger.exception(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


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