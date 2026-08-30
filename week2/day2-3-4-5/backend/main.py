from fastapi import FastAPI, HTTPException

from backend.schemas import QuestionRequest, AnswerResponse
from backend.logger import logger

from rag_pipeline import ask_question as rag_ask


app = FastAPI(
    title="PDF Chat Assistant API"
)


@app.get("/")
def root():
    return {
        "message": "PDF Chat Assistant API is running"
    }


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):

    try:
        logger.info(
            f"Question received: {request.question}"
        )

        result = rag_ask(request.question)

        logger.info(
            "Answer generated successfully"
        )

        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception as e:

        logger.error(
            f"Error generating answer: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Error generating answer"
        )