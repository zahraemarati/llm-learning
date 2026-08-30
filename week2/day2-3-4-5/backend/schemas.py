from pydantic import BaseModel
from typing import Any


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[Any] = []