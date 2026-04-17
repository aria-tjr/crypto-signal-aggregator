import sys
import os

# افزودن بوم پروژه به path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🧪 تست نصب و تنظیمات")
print("=" * 60)

# تست Python version
print(f"\n✅ Python Version: {sys.version}")

# تست Virtual Environment
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("✅ Virtual Environment: فعال")
else:
    print("⚠️ Virtual Environment: غیر فعال (توصیه می‌شود فعال کنید)")

# تست imports
print("\n📦 تست کتابخانه‌ها:")

libraries = {
    'pandas': 'Pandas (Data Analysis)',
    'numpy': 'NumPy (Numerical Computing)',
    'ccxt': 'CCXT (Exchange APIs)',
    'talib': 'TA-Lib (Technical Analysis)',
    'ta': 'TA (Technical Analysis)',
    'sklearn': 'Scikit-learn (Machine Learning)',
    'xgboost': 'XGBoost (ML Model)',
    'tensorflow': 'TensorFlow (Deep Learning)',
    'telegram': 'Python Telegram Bot',
    'praw': 'PRAW (Reddit API)',
    'vaderSentiment': 'VADER Sentiment',
    'nltk': 'NLTK (NLP)',
    'openai': 'OpenAI API',
    'aiohttp': 'Aiohttp (Async HTTP)',
    'redis': 'Redis',
}

failed = []

for lib, display_name in libraries.items():
    try:
        __import__(lib)
        print(f"   ✅ {display_name}")
    except ImportError as e:
        print(f"   ❌ {display_name}: {e}")
        failed.append(lib)

# تست Configuration
print("\n⚙️ تست Configuration:")

try:
    from config.settings import (
        TELEGRAM_TOKEN, TELEGRAM_CHAT_ID,
        REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET,
        OPENAI_API_KEY, BOT_WEIGHTS
    )
    
    settings_check = {
        'TELEGRAM_TOKEN': bool(TELEGRAM_TOKEN),
        'TELEGRAM_CHAT_ID': bool(TELEGRAM_CHAT_ID),
        'REDDIT_CLIENT_ID': bool(REDDIT_CLIENT_ID),
        'REDDIT_CLIENT_SECRET': bool(REDDIT_CLIENT_SECRET),
        'OPENAI_API_KEY': bool(OPENAI_API_KEY),
    }
    
    for setting, value in settings_check.items():
        status = "✅" if value else "⚠️"
        print(f"   {status} {setting}: {'Set' if value else 'NOT SET'}")
    
    print(f"   ✅ BOT_WEIGHTS: {len(BOT_WEIGHTS)} بات")
    
except Exception as e:
    print(f"   ❌ Error loading settings: {e}")

# خلاصه
print("\n" + "=" * 60)

if not failed:
    print("🎉 تمام تست‌ها موفق! پروژه آماده برای اجرا است.")
else:
    print(f"❌ {len(failed)} کتابخانه نصب نشده:")
    for lib in failed:
        print(f"   - {lib}")
    print("\nدستور نصب:")
    print(f"   pip install {' '.join(failed)}")

print("=" * 60)
