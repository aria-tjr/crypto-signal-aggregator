# استفاده از Python 3.9
FROM python:3.9-slim

# تنظیم working directory
WORKDIR /app

# نصب dependencies سیستمی
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# اختیاری: نصب TA-Lib (ممکن است در توزیع پایه موجود نباشد)
# اگر نیاز دارید، بسته‌های مورد نیاز را اضافه یا از منبع نصب کنید.
# RUN apt-get update && apt-get install -y ta-lib || true

# کپی requirements
COPY requirements.txt .

# نصب Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# کپی تمام فایل‌های پروژه
COPY . .

# ایجاد پوشه‌های لازم
RUN mkdir -p logs data

# Healthcheck (برای /health)
HEALTHCHECK --interval=60s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# اجرای برنامه
CMD ["python", "main.py"]
