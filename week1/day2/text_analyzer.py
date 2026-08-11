from openai import OpenAI
import json


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


text = input("متن خود را وارد کنید:\n> ")


response = client.chat.completions.create(
    model="llama3",

    messages=[
        # Role Prompting
        {
            "role": "system",
            "content": """
تو یک متخصص تحلیل متن هستی.

وظیفه تو این است که متن کاربر را تحلیل کنی.

خروجی باید شامل موارد زیر باشد:

title:
یک عنوان کوتاه برای متن

summary:
خلاصه متن در حداکثر دو جمله

keywords:
بین 3 تا 5 کلمه یا عبارت کلیدی

sentiment:
فقط یکی از مقادیر زیر:
positive
negative
neutral

فقط JSON برگردان.
"""
        },

        # Few-shot Example 1
        {
            "role": "user",
            "content": """
امروز گوشی جدیدم رسید.
کیفیت دوربین فوق‌العاده است و از سرعت دستگاه خیلی راضی هستم.
"""
        },

        {
            "role": "assistant",
            "content": """
{
    "title": "رضایت از گوشی جدید",
    "summary": "کاربر از کیفیت دوربین و سرعت گوشی جدید خود رضایت دارد.",
    "keywords": ["گوشی", "دوربین", "سرعت", "رضایت"],
    "sentiment": "positive"
}
"""
        },

        # Few-shot Example 2
        {
            "role": "user",
            "content": """
سفارش من سه روز دیر رسید و بسته‌بندی محصول هم آسیب دیده بود.
"""
        },

        {
            "role": "assistant",
            "content": """
{
    "title": "نارضایتی از سفارش",
    "summary": "سفارش با تأخیر رسیده و بسته‌بندی محصول نیز آسیب دیده است.",
    "keywords": ["سفارش", "تأخیر", "بسته‌بندی", "آسیب"],
    "sentiment": "negative"
}
"""
        },

        # متن واقعی کاربر
        {
            "role": "user",
            "content": text
        }
    ],

    # Structured Output
    response_format={
        "type": "json_object"
    },

    temperature=0
)


result = response.choices[0].message.content

data = json.loads(result)


print("\n--- نتیجه تحلیل ---")

print("عنوان:")
print(data["title"])

print("\nخلاصه:")
print(data["summary"])

print("\nکلمات کلیدی:")
print(data["keywords"])

print("\nاحساس:")
print(data["sentiment"])