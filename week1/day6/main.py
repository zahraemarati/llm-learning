from chat import ask
from summarize import summarize_text, summarize_conversation
from extract import extract_info
from memory import ConversationMemory

HELP_TEXT = """
دستورات:
  /summarize <متن>   → خلاصه کردن یک متن دلخواه
  /extract <متن>     → استخراج اطلاعات از یک متن
  /history           → خلاصه کردن کل مکالمه‌ی فعلی
  /help              → نمایش همین راهنما
  exit               → خروج از برنامه

هر چیز دیگه‌ای که بنویسی، به عنوان پیام چت عادی به دستیار فرستاده می‌شه.
"""

def main():
    print("=== AI Assistant v1 ===")
    print(HELP_TEXT)

    while True:
        user_input = input("شما: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("خداحافظ!")
            break

        if user_input == "/help":
            print(HELP_TEXT)
            continue

        if user_input.startswith("/summarize "):
            text = user_input[len("/summarize "):].strip()
            if not text:
                print("لطفاً بعد از /summarize یک متن بنویس.\n")
                continue
            try:
                result = summarize_text(text)
                print(f"\nخلاصه:\n{result}\n")
            except Exception as e:
                print(f"\nخطا در خلاصه‌سازی: {e}\n")
            continue

        if user_input.startswith("/extract "):
            text = user_input[len("/extract "):].strip()
            if not text:
                print("لطفاً بعد از /extract یک متن بنویس.\n")
                continue
            try:
                info = extract_info(text)
                print(f"\nاطلاعات استخراج‌شده:\n{info.model_dump_json(indent=2, ensure_ascii=False)}\n")
            except Exception as e:
                print(f"\nخطا در استخراج اطلاعات: {e}\n")
            continue

        if user_input == "/history":
            from chat import memory as chat_memory
            try:
                result = summarize_conversation(chat_memory.get_messages())
                print(f"\nخلاصه‌ی مکالمه تا الان:\n{result}\n")
            except Exception as e:
                print(f"\nخطا در خلاصه‌سازی مکالمه: {e}\n")
            continue

        # پیام چت عادی
        try:
            reply = ask(user_input)
            print(f"دستیار: {reply}\n")
        except Exception as e:
            print(f"خطا در دریافت پاسخ: {e}\n")


if __name__ == "__main__":
    main()