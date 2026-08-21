# AI Assistant v1

دستیار هوشمند مبتنی بر LLM با قابلیت‌های چت، خلاصه‌سازی، استخراج اطلاعات و حافظه‌ی مکالمه.

## تکنولوژی
- Python 3.10+
- OpenAI SDK (متصل به OpenRouter)
- python-dotenv
- Pydantic

## نصب

\`\`\`bash
python -m venv venv
source venv/bin/activate  # ویندوز: venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

## تنظیمات

یک فایل `.env` در ریشه‌ی پروژه بساز:

\`\`\`
OPENROUTER_API_KEY=sk-or-v1-...
CHAT_MODEL=google/gemma-4-31b-it:free
EMBED_MODEL=nvidia/nemotron-3-embed-1b:free
\`\`\`

## اجرا

\`\`\`bash
python3 main.py
\`\`\`

## دستورات داخل برنامه

| دستور | کاربرد |
|---|---|
| `/summarize <متن>` | خلاصه کردن یک متن |
| `/extract <متن>` | استخراج موضوع، احساس، اسامی و اقدامات لازم از متن |
| `/history` | خلاصه کردن کل مکالمه تا این لحظه |
| `/help` | نمایش راهنما |
| `exit` | خروج |

## ساختار پروژه

\`\`\`
day6/
├── main.py           # نقطه‌ی ورود اصلی
├── chat.py           # منطق چت + حافظه
├── memory.py         # کلاس ConversationMemory
├── summarize.py       # خلاصه‌سازی متن/مکالمه
├── extract.py         # استخراج اطلاعات ساختاریافته (Pydantic)
├── config.py          # تنظیمات از .env
├── requirements.txt
├── .env               # (در گیت‌هاب قرار نمی‌گیرد)
└── data/              # اسناد نمونه‌ی شرکت (برای فاز بعدی RAG)
\`\`\`

## محدودیت‌های شناخته‌شده
- از مدل رایگان `google/gemma-4-31b-it:free` روی OpenRouter استفاده می‌شود که ممکن است گاهی rate-limit شود (کد retry دارد).
- فاز RAG (پاسخ بر اساس مستندات شرکت) هنوز پیاده‌سازی نشده و برای نسخه‌ی بعدی برنامه‌ریزی شده.