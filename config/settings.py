import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

# ==========================================
# TELEGRAM SETTINGS
# ==========================================
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# ==========================================
# EXCHANGE SETTINGS
# ==========================================
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
BINANCE_TEST_MODE = os.getenv('BINANCE_TEST_MODE', 'False') == 'True'

KUCOIN_API_KEY = os.getenv('KUCOIN_API_KEY')
KUCOIN_API_SECRET = os.getenv('KUCOIN_API_SECRET')
KUCOIN_PASSPHRASE = os.getenv('KUCOIN_PASSPHRASE')

# ==========================================
# REDDIT SETTINGS
# ==========================================
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'crypto_signal_bot/1.0')

# ==========================================
# TWITTER SETTINGS
# ==========================================
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')

# ==========================================
# AI/LLM SETTINGS
# ==========================================
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# ==========================================
# BOT CONFIGURATION
# ==========================================
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 300))
MIN_CONFIDENCE = float(os.getenv('MIN_CONFIDENCE', 0.75))
MAX_CONFIDENCE = float(os.getenv('MAX_CONFIDENCE', 0.95))
DEBUG = os.getenv('DEBUG', 'True') == 'True'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# ==========================================
# DEFAULT SYMBOLS
# ==========================================
DEFAULT_SYMBOLS = os.getenv(
    'DEFAULT_SYMBOLS',
    'BTC/USDT,ETH/USDT,SOL/USDT,DOGE/USDT,XRP/USDT'
).split(',')

# ==========================================
# API ENDPOINTS
# ==========================================
COINGECKO_API = os.getenv('COINGECKO_API', 'https://api.coingecko.com/api/v3')
GLASSNODE_API_KEY = os.getenv('GLASSNODE_API_KEY')

# ==========================================
# DATABASE
# ==========================================
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./crypto_signals.db')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# ==========================================
# BOT NAMES & WEIGHTS
# ==========================================
BOT_WEIGHTS = {
    'technical_basic': 0.15,
    'technical_advanced': 0.15,
    'ml_prediction': 0.12,
    'onchain': 0.12,
    'sentiment': 0.12,
    'volume': 0.10,
    'volatility': 0.10,
    'correlation': 0.08,
    'macro': 0.08,
    'ai': 0.08
}

BOT_NAMES = {
    'technical_basic': '1️⃣ تکنیکال پایه‌ای',
    'technical_advanced': '2️⃣ تکنیکال پیشرفته',
    'ml_prediction': '3️⃣ ML Prediction',
    'onchain': '4️⃣ On-Chain Analysis',
    'sentiment': '5️⃣ Sentiment Analysis',
    'volume': '6️⃣ Volume Analysis',
    'volatility': '7️⃣ Volatility Analysis',
    'correlation': '8️⃣ Correlation Analysis',
    'macro': '9️⃣ Macro Indicators',
    'ai': '🔟 AI Analysis'
}

# ==========================================
# VALIDATION
# ==========================================
def validate_settings():
    """بررسی تنظیمات ضروری"""
    required_settings = {
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
        'REDDIT_CLIENT_ID': REDDIT_CLIENT_ID,
        'REDDIT_CLIENT_SECRET': REDDIT_CLIENT_SECRET,
        'OPENAI_API_KEY': OPENAI_API_KEY,
    }
    
    missing = [k for k, v in required_settings.items() if not v]
    
    if missing:
        raise ValueError(f"❌ Settings مفقود: {', '.join(missing)}")
    
    return True
