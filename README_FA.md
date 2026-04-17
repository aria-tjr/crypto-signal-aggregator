# 🤖 Crypto Signal Bot - بات تولید کننده سیگنال معاملات

## تحلیل معاملات فیوچرز با ۱۰ منبع تخصصی

### ویژگی‌ها

- ✅ **۱۰ بات تحلیلی مستقل** برای دقت بیشتر
- ✅ **تحلیل تکنیکال** (پایه‌ای و پیشرفته)
- ✅ **پیش‌بینی قیمت** با Machine Learning
- ✅ **تحلیل On-Chain** (جریان توکن‌ها)
- ✅ **تحلیل احساسات** (Reddit، Twitter)
- ✅ **تحلیل حجم معاملات**
- ✅ **تحلیل نوسان‌پذیری**
- ✅ **تحلیل کلان‌اقتصادی**
- ✅ **تحلیل هوشمند** با GPT-4
- ✅ **Telegram Integration** برای اطلاع‌رسانی

### نیازمندی‌ها

- Python 3.9+
- pip
- Virtual Environment

### نصب

```
# 1. Clone repository
git clone <your-repo>
cd crypto_signal_bot

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup .env file
cp .env.example .env
# ویرایش .env با API Keys خود

# 5. Test setup
python test_setup.py

# 6. Run
python main.py
```

### استفاده

```
/start - شروع بات
/signal BTC/USDT - تولید سیگنال
/monitor - نظارت خودکار
/list - لیست سکه‌ها
/status - وضعیت
/help - راهنما
```

### ساختار پروژه

```
crypto_signal_bot/
├── bots/                 # ۱۰ بات تخصصی
├── aggregator/           # ادغام سیگنال‌ها
├── telegram/             # Telegram bot
├── data_fetchers/        # منابع داده
├── database/             # دیتابیس
├── utils/                # ابزارهای کمکی
├── config/               # تنظیمات
├── logs/                 # لاگ‌ها
├── .env                  # متغیرهای محیطی
├── requirements.txt      # وابستگی‌ها
├── main.py               # نقطه شروع
└── test_setup.py         # تست نصب
```

### لایسنس

MIT

### مساعد

برای سؤالات: [Email یا Link]
