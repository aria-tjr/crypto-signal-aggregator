import asyncio
import logging

from tg_bot import CryptoSignalTelegramBot

logging.basicConfig(level=logging.INFO)


async def test_bot():
    print("\n🧪 Testing Telegram Bot (non-polling parts)...\n")

    try:
        bot = CryptoSignalTelegramBot()
        print("✅ Bot initialized successfully")
        print(f"   Chat ID: {bot.chat_id}")
        print(f"   Monitored symbols: {bot.monitored_symbols}")

        # تجمیع سیگنال برای یک سکه
        print("\n📊 Testing signal generation...")
        result = await bot.aggregator.aggregate_signals('BTC/USDT')

        print(f"   Recommendation: {result['recommendation']}")
        print(f"   Confidence: {result['confidence_score']:.1%}")

        # فرمت برای Telegram
        print("\n🎨 Testing message formatting...")
        message = bot.formatter.format_for_telegram(result)
        print("✅ Message formatted successfully")
        print(f"   Length: {len(message)} characters")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_bot())
