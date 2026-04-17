"""
تست سیستم کامل
"""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from aggregator import HybridSignalAggregator
from tg_bot import CryptoSignalTelegramBot
from utils.logger import setup_logger

logger = setup_logger("SystemTest")


async def test_aggregator() -> bool:
    """تست Aggregator (happy path on a common symbol)."""

    logger.info("\n" + "=" * 70)
    logger.info("🧪 Testing Signal Aggregator")
    logger.info("=" * 70)

    try:
        aggregator = HybridSignalAggregator()
        logger.info("✅ Aggregator initialized")

        # تست سیگنال
        logger.info("📊 Testing signal generation for BTC/USDT...")
        result = await aggregator.aggregate_signals("BTC/USDT")

        logger.info("✅ Signal generated successfully")
        logger.info(f"   Recommendation: {result['recommendation']}")
        logger.info(f"   Confidence: {result['confidence_score']:.1%}")
        logger.info(f"   Valid Sources: {result['valid_sources']}/10")

        return True

    except Exception as e:
        logger.error(f"❌ Aggregator test failed: {e}")
        return False


async def test_telegram_bot() -> bool:
    """تست Telegram Bot (only initialization & formatting)."""

    logger.info("\n" + "=" * 70)
    logger.info("🧪 Testing Telegram Bot")
    logger.info("=" * 70)

    # Skip if env is not configured
    if not (os.getenv("TELEGRAM_TOKEN") and os.getenv("TELEGRAM_CHAT_ID")):
        logger.warning("⚠️  Skipping Telegram Bot test (missing TELEGRAM_TOKEN/TELEGRAM_CHAT_ID)")
        return True

    try:
        bot = CryptoSignalTelegramBot()
        logger.info("✅ Bot initialized")

        # بررسی formatter
        sample_result = {
            "symbol": "BTC/USDT",
            "timestamp": "2025-11-02T15:54:00",
            "recommendation": "BUY",
            "confidence_score": 0.85,
            "valid_sources": 9,
            "execution_time": 8.5,
            "bot_signals": {
                "technical_basic": {"signal": 1, "confidence": 0.9},
                "technical_advanced": {"signal": 1, "confidence": 0.85},
                "ml_prediction": {"signal": 1, "confidence": 0.8},
                "onchain": {"signal": 1, "confidence": 0.75},
                "sentiment": {"signal": 1, "confidence": 0.8},
                "volume": {"signal": 1, "confidence": 0.75},
                "volatility": {"signal": 0, "confidence": 0.5},
                "correlation": {"signal": 1, "confidence": 0.7},
                "macro": {"signal": 1, "confidence": 0.8},
                "ai": {"signal": 1, "confidence": 0.85},
            },
        }

        message = bot.formatter.format_for_telegram(sample_result)
        logger.info("✅ Message formatted successfully")
        logger.info(f"   Message length: {len(message)} characters")

        return True

    except Exception as e:
        logger.error(f"❌ Bot test failed: {e}")
        return False


async def test_full_system() -> bool:
    """تست سیستم کامل"""

    logger.info("\n" + "=" * 80)
    logger.info("🧪 Full System Test")
    logger.info("=" * 80)

    # بارگذاری .env
    load_dotenv()
    logger.info("✅ .env loaded")

    # تست‌ها
    tests = [
        ("Aggregator", test_aggregator),
        ("Telegram Bot", test_telegram_bot),
    ]

    results: dict[str, bool] = {}

    for test_name, test_func in tests:
        try:
            logger.info(f"\n🧪 Running: {test_name}")
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"❌ {test_name} test failed: {e}")
            results[test_name] = False

    # خلاصه
    logger.info("\n" + "=" * 80)
    logger.info("📊 Test Summary")
    logger.info("=" * 80)

    passed = sum(1 for r in results.values() if r)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")

    logger.info(f"\n📈 Overall: {passed}/{total} tests passed")

    if passed == total:
        logger.info("\n🎉 All tests passed! System is ready to run.")
        return True
    else:
        logger.warning("\n⚠️  Some tests failed. Check configuration.")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(test_full_system())
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)
