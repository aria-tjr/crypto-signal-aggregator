"""
🎨 Signal Formatter - فرمت‌کردن سیگنال‌ها برای خروجی
"""

from __future__ import annotations

import logging
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class SignalFormatter:
    """
    فرمت‌کردن سیگنال‌های تجمیع‌شده برای مختلف خروجی‌ها
    """

    @staticmethod
    def format_for_telegram(result: Dict) -> str:
        """
        فرمت‌کردن برای Telegram Bot
        """

        symbol = result["symbol"]
        recommendation = result["recommendation"]
        confidence = result["confidence_score"]
        valid_sources = result["valid_sources"]
        bot_signals = result["bot_signals"]

        # Emoji بر اساس سیگنال
        emoji_map = {"BUY": "🟢", "SELL": "🔴", "HOLD": "⚪"}
        emoji = emoji_map.get(recommendation, "⚪")

        # بخش اول: خلاصه
        message = (
            f"\n<b>{emoji} {recommendation} {symbol} {emoji}</b>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>📊 خلاصه کلی:</b>\n"
            f"🎯 توصیه: <code>{recommendation}</code>\n"
            f"📈 نمره اعتماد: <code>{confidence*100:.1f}%</code>\n"
            f"✅ منابع موافق: <code>{valid_sources}/10</code>\n"
            f"⏱️  زمان اجرا: <code>{result.get('execution_time', 0):.2f}s</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>🔍 تفاصیل ۱۰ منبع:</b>\n"
        )

        # بخش دوم: جزئیات هر بات
        bot_display_names = {
            "technical_basic": "1️⃣ تکنیکال پایه‌ای",
            "technical_advanced": "2️⃣ تکنیکال پیشرفته",
            "ml_prediction": "3️⃣ ML Prediction",
            "onchain": "4️⃣ On-Chain Analysis",
            "sentiment": "5️⃣ Sentiment Analysis",
            "volume": "6️⃣ Volume Analysis",
            "volatility": "7️⃣ Volatility Analysis",
            "correlation": "8️⃣ Correlation Analysis",
            "macro": "9️⃣ Macro Indicators",
            "ai": "🔟 AI Analysis",
        }

        for bot_key in [
            "technical_basic",
            "technical_advanced",
            "ml_prediction",
            "onchain",
            "sentiment",
            "volume",
            "volatility",
            "correlation",
            "macro",
            "ai",
        ]:
            if bot_key in bot_signals:
                signal_data = bot_signals[bot_key]

                if "error" in signal_data:
                    message += f"<b>{bot_display_names[bot_key]}</b> ❌ (خطا)\n"
                else:
                    signal = int(signal_data.get("signal", 0))
                    confidence_val = float(signal_data.get("confidence", 0))

                    signal_emoji = {1: "🟢", -1: "🔴", 0: "⚪"}.get(signal, "⚪")

                    message += (
                        f"<b>{bot_display_names[bot_key]}</b> {signal_emoji} "
                        f"({confidence_val*100:.0f}%)\n"
                    )

        # بخش سوم: توصیه نهایی
        message += (
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>✨ توصیه نهایی:</b>\n<code>{recommendation}</code>\n\n"
            f"<b>⚠️ نکات مهم:</b>\n"
            "• این فقط توصیه‌ای است\n"
            "• خود تصمیم‌گیری ضروری است\n"
            "• ریسک مدیریت کنید\n"
            "• Leverage مناسب تنظیم کنید\n\n"
            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        return message

    @staticmethod
    def format_for_json(result: Dict) -> Dict:
        """
        فرمت‌کردن برای JSON Export
        """

        return {
            "symbol": result["symbol"],
            "timestamp": result["timestamp"],
            "recommendation": result["recommendation"],
            "confidence_score": round(result["confidence_score"], 4),
            "valid_sources": result["valid_sources"],
            "bot_signals": {
                bot_key: {
                    "signal": signal_data.get("signal", 0),
                    "confidence": round(signal_data.get("confidence", 0), 4),
                }
                for bot_key, signal_data in result["bot_signals"].items()
                if "error" not in signal_data
            },
            "execution_time": round(result.get("execution_time", 0), 2),
        }

    @staticmethod
    def format_for_csv(result: Dict) -> str:
        """
        فرمت‌کردن برای CSV Export
        """

        line = (
            f"{result['timestamp']},{result['symbol']},{result['recommendation']},"
            f"{result['confidence_score']:.4f},{result['valid_sources']}"
        )

        for bot_key in [
            "technical_basic",
            "technical_advanced",
            "ml_prediction",
            "onchain",
            "sentiment",
            "volume",
            "volatility",
            "correlation",
            "macro",
            "ai",
        ]:
            if bot_key in result["bot_signals"]:
                signal_data = result["bot_signals"][bot_key]
                signal = int(signal_data.get("signal", 0))
                line += f",{signal}"

        return line


# ===== Test =====
if __name__ == "__main__":
    sample_result = {
        "symbol": "BTC/USDT",
        "timestamp": datetime.now().isoformat(),
        "recommendation": "BUY",
        "confidence_score": 0.85,
        "valid_sources": 9,
        "execution_time": 8.5,
        "bot_signals": {
            "technical_basic": {"signal": 1, "confidence": 0.9},
            "technical_advanced": {"signal": 1, "confidence": 0.85},
            "ml_prediction": {"signal": 1, "confidence": 0.8},
        },
    }

    formatter = SignalFormatter()
    telegram_msg = formatter.format_for_telegram(sample_result)
    print(telegram_msg)
