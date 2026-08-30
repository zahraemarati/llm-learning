from fastapi import FastAPI, HTTPException, UploadFile, File
from vector_store.chroma_db import create_vector_store
import shutil
import os
from backend.schemas import QuestionRequest, AnswerResponse
from backend.logger import logger

from rag_pipeline import ask_question as rag_ask


app = FastAPI(
    title="PDF Chat Assistant API"
)

import os
import shutil

from fastapi import FastAPI, HTTPException, UploadFile, File

from backend.schemas import QuestionRequest, AnswerResponse
from backend.logger import logger

from vector_store.chroma_db import create_vector_store
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

    except Exception:

        logger.exception(
            "Error generating answer"
        )

        raise HTTPException(
            status_code=500,
            detail="Error generating answer"
        )


@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):

    try:
        upload_dir = "uploads"

        os.makedirs(
            upload_dir,
            exist_ok=True
        )

        file_path = f"{upload_dir}/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        result = create_vector_store(
            file_path
        )

        logger.info(
            f"PDF uploaded: {file.filename}"
        )

        return result

    except Exception:

        logger.exception(
            "PDF upload failed"
        )

        raise HTTPException(
            status_code=500,
            detail="PDF processing failed"
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

@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):

    try:
        upload_dir = "uploads"

        os.makedirs(
            upload_dir,
            exist_ok=True
        )

        file_path = f"{upload_dir}/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        result = create_vector_store(
            file_path
        )

        logger.info(
            f"PDF uploaded: {file.filename}"
        )

        return result


    except Exception as e:

        logger.exception(
            "PDF upload failed"
        )

        raise HTTPException(
            status_code=500,
            detail="PDF processing failed"
        )