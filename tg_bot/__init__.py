"""
Telegram Module - بات تلگرام (renamed to avoid PTB shadowing)

این پکیج به جای نام «telegram» از «tg_bot» استفاده می‌کند تا با پکیج
python-telegram-bot تداخل نام نداشته باشد.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

__all__ = ["CryptoSignalTelegramBot"]


def __getattr__(name: str):
    if name == "CryptoSignalTelegramBot":
        try:
            from .telegram_bot import CryptoSignalTelegramBot  # lazy import
            logger.info("✅ CryptoSignalTelegramBot loaded")
            return CryptoSignalTelegramBot
        except Exception as e:
            logger.error(f"❌ Error loading CryptoSignalTelegramBot: {e}")
            raise
    raise AttributeError(name)
