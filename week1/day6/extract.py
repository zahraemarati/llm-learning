from typing import Literal
import json
from pydantic import BaseModel, Field, ValidationError
from llm_client import chat_complete

class ExtractedInfo(BaseModel):
    topic: str = Field(description="موضوع اصلی متن")
    sentiment: Literal["مثبت", "منفی", "خنثی"] = Field(description="احساس کلی متن")
    entities: list[str] = Field(description="اسامی افراد، شرکت‌ها یا مکان‌های ذکرشده")
    action_items: list[str] = Field(default_factory=list, description="اگر کاری باید انجام شود")

def extract_info(text: str, retries: int = 2) -> ExtractedInfo:
    prompt = (
        "اطلاعات زیر را از متن استخراج کن و فقط یک JSON خام (بدون ```json و بدون توضیح اضافه) "
        "با این ساختار دقیق برگردان. مقدار sentiment باید دقیقاً یکی از این سه کلمه باشد: "
        '"مثبت"، "منفی"، "خنثی".\n'
        '{"topic": "...", "sentiment": "...", "entities": ["..."], "action_items": ["..."]}\n\n'
        f"متن:\n{text}"
    )
    last_error = None
    for attempt in range(retries + 1):
        raw = chat_complete([{"role": "user", "content": prompt}]).strip()
        raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            data = json.loads(raw)
            return ExtractedInfo(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            last_error = e
            continue
    raise ValueError(f"مدل نتونست خروجی معتبر تولید کنه بعد از {retries + 1} تلاش: {last_error}")