from pydantic import BaseModel
from typing import Any


class QuestionRequest(BaseModel):
    question: str
    min_page: int | None = None
    max_page: int | None = None


class AnswerResponse(BaseModel):
    answer: str
    sources: list[Any] = []