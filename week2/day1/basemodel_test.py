from pydantic import BaseModel


class LLMResponse(BaseModel):
    answer: str
    confidence: float
    sources: list[str]
    is_safe: bool


response = LLMResponse(
    answer="پاسخ سوال",
    confidence=0.95,
    sources=["doc1", "doc2"],
    is_safe=True
)


response = LLMResponse(
    answer=123,
    confidence="high",
    sources="document",
    is_safe="yes"
)




