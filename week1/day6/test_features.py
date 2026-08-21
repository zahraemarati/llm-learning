from summarize import summarize_text
from extract import extract_info

sample = """
سلام، من علی هستم از شرکت نوین‌سافت تماس می‌گیرم. ما یک مشکل جدی با سیستم فاکتورهای الکترونیکی داریم،
سه روزه که فاکتورها به سامانه‌ی مودیان ارسال نمی‌شن و مشتری‌های ما شاکی هستن. لطفاً هرچه سریع‌تر
یک نفر از تیم پشتیبانی باهام تماس بگیره. ضمناً خیلی از این تأخیر ناراحتم.
"""

print("خلاصه:")
print(summarize_text(sample))

print("\nاطلاعات استخراج‌شده:")
info = extract_info(sample)
print(info.model_dump_json(indent=2, ensure_ascii=False))

