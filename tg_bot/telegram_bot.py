"""
🤖 Telegram Bot - تولید و ارسال سیگنال‌های معاملات
(Renamed package to tg_bot to avoid shadowing python-telegram-bot's telegram)
"""

from __future__ import annotations

import logging
import asyncio
from datetime import datetime
from typing import Dict, List

from aggregator import HybridSignalAggregator, SignalFormatter, SignalValidator
from config.settings import (
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
    DEFAULT_SYMBOLS,
    MIN_CONFIDENCE,
)

# Import python-telegram-bot directly (no name conflict now)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class CryptoSignalTelegramBot:
    """بات تلگرام برای تولید و ارسال سیگنال‌های معاملات"""

    def __init__(self) -> None:
        if not TELEGRAM_TOKEN:
            raise ValueError("❌ TELEGRAM_TOKEN not set in .env")
        if not TELEGRAM_CHAT_ID:
            raise ValueError("❌ TELEGRAM_CHAT_ID not set in .env")

        self.token = TELEGRAM_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID

        # Aggregator/Formatter/Validator
        self.aggregator = HybridSignalAggregator()
        self.formatter = SignalFormatter()
        self.validator = SignalValidator()

        # Monitored symbols
        self.monitored_symbols = list(DEFAULT_SYMBOLS)

        # Application
        self.application = Application.builder().token(self.token).build()

        # State
        self.is_monitoring: bool = False
        self.monitoring_interval: int = 300  # seconds

        logger.info("✅ CryptoSignalTelegramBot initialized")

    def setup_handlers(self) -> None:
        logger.info("📋 Setting up command handlers...")

        self.application.add_handler(CommandHandler("start", self.cmd_start))
        self.application.add_handler(CommandHandler("signal", self.cmd_signal))
        self.application.add_handler(CommandHandler("monitor", self.cmd_monitor))
        self.application.add_handler(CommandHandler("stop", self.cmd_stop_monitor))
        self.application.add_handler(CommandHandler("add", self.cmd_add_symbol))
        self.application.add_handler(CommandHandler("remove", self.cmd_remove_symbol))
        self.application.add_handler(CommandHandler("list", self.cmd_list_symbols))
        self.application.add_handler(CommandHandler("status", self.cmd_status))
        self.application.add_handler(CommandHandler("help", self.cmd_help))
        self.application.add_handler(CommandHandler("stats", self.cmd_stats))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))

        logger.info("✅ Command handlers set up")

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        welcome_text = """
╔════════════════════════════════════════════════╗
║   🤖 بات سیگنال معاملات فیوچرز 🤖             ║
║   Crypto Trading Signal Generator             ║
║   با ۱۰ منبع تحلیلی تخصصی                    ║
╚════════════════════════════════════════════════╝

برای شروع /help را بزنید یا /signal BTC/USDT را امتحان کنید.
"""
        keyboard = [
            [InlineKeyboardButton("📊 سیگنال", callback_data="action_signal"),
             InlineKeyboardButton("🔔 نظارت", callback_data="action_monitor")],
            [InlineKeyboardButton("📋 دستورات", callback_data="action_help"),
             InlineKeyboardButton("📈 آمار", callback_data="action_stats")],
        ]
        await update.message.reply_text(welcome_text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

    async def cmd_signal(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args:
            await update.message.reply_text(
                "❌ <b>لطفا سکه را مشخص کنید</b>\n\nمثال‌ها:\n/signal BTC/USDT\n/signal ETH/USDT",
                parse_mode="HTML",
            )
            return
        symbol = context.args[0].upper()
        status_msg = await update.message.reply_text(f"⏳ <b>تجزیه‌وتحلیل {symbol}...</b>", parse_mode="HTML")
        try:
            result = await self.aggregator.aggregate_signals(symbol)
            await status_msg.edit_text(self.formatter.format_for_telegram(result), parse_mode="HTML")
        except Exception as e:
            logger.error(f"❌ Error generating signal: {e}")
            await status_msg.edit_text(f"❌ <b>خطا:</b> {e}", parse_mode="HTML")

    async def cmd_monitor(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if self.is_monitoring:
            await update.message.reply_text("⚠️ <b>نظارت خودکار قبلا فعال است</b>\n\nبرای متوقف کردن: /stop", parse_mode="HTML")
            return
        self.is_monitoring = True
        await update.message.reply_text("🔔 <b>نظارت خودکار فعال شد!</b>", parse_mode="HTML")
        context.application.create_task(self._monitoring_loop())

    async def cmd_stop_monitor(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.is_monitoring:
            await update.message.reply_text("⚠️ <b>نظارت خودکار فعال نیست</b>\n\nبرای شروع: /monitor", parse_mode="HTML")
            return
        self.is_monitoring = False
        await update.message.reply_text("⛔ <b>نظارت خودکار متوقف شد</b>", parse_mode="HTML")

    async def cmd_add_symbol(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args:
            await update.message.reply_text("❌ <b>لطفا سکه را مشخص کنید</b>\n\nمثال: /add DOGE/USDT", parse_mode="HTML")
            return
        symbol = context.args[0].upper()
        if symbol in self.monitored_symbols:
            await update.message.reply_text(f"⚠️ <b>{symbol} قبلا در لیست وجود دارد</b>", parse_mode="HTML")
            return
        self.monitored_symbols.append(symbol)
        await update.message.reply_text(f"✅ <b>{symbol} اضافه شد</b>", parse_mode="HTML")

    async def cmd_remove_symbol(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args:
            await update.message.reply_text("❌ <b>لطفا سکه را مشخص کنید</b>\n\nمثال: /remove DOGE/USDT", parse_mode="HTML")
            return
        symbol = context.args[0].upper()
        if symbol not in self.monitored_symbols:
            await update.message.reply_text(f"⚠️ <b>{symbol} در لیست وجود ندارد</b>", parse_mode="HTML")
            return
        self.monitored_symbols.remove(symbol)
        await update.message.reply_text(f"✅ <b>{symbol} حذف شد</b>", parse_mode="HTML")

    async def cmd_list_symbols(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.monitored_symbols:
            await update.message.reply_text("📋 <b>لیست سکه‌ها خالی است</b>", parse_mode="HTML")
            return
        message = "📋 <b>سکه‌های تحت نظارت:</b>\n\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(self.monitored_symbols))
        await update.message.reply_text(message, parse_mode="HTML")

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        monitoring_status = "🟢 فعال" if self.is_monitoring else "🔴 غیرفعال"
        msg = f"""
<b>📊 وضعیت سیستم</b>

<b>بات:</b>
✅ بات تلگرام: فعال
✅ Aggregator: فعال

<b>نظارت:</b>
{monitoring_status}
📈 سکه‌ها: {len(self.monitored_symbols)}
⏱️ بازه: {self.monitoring_interval}s
"""
        await update.message.reply_text(msg, parse_mode="HTML")

    async def cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        stats = self.aggregator.get_statistics()
        msg = f"""
📈 <b>آمار تحلیل‌ها</b>
کل: {stats['total_analyses']}
موفق: {stats['successful_analyses']}
نرخ موفقیت: {stats['success_rate']:.1f}%
⏰ آخرین: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        await update.message.reply_text(msg, parse_mode="HTML")

    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("/signal BTC/USDT, /monitor, /stop, /list, /status, /stats", parse_mode="HTML")

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        if query.data == "action_monitor" and not self.is_monitoring:
            self.is_monitoring = True
            await query.edit_message_text("🟢 نظارت فعال شد", parse_mode="HTML")
            context.application.create_task(self._monitoring_loop())

    async def _monitoring_loop(self) -> None:
        logger.info("🔔 Monitoring loop started")
        while self.is_monitoring:
            try:
                for symbol in self.monitored_symbols:
                    try:
                        result = await self.aggregator.aggregate_signals(symbol)
                        if result["confidence_score"] >= MIN_CONFIDENCE and result["recommendation"] != "HOLD":
                            await self.application.bot.send_message(
                                chat_id=self.chat_id,
                                text=self.formatter.format_for_telegram(result),
                                parse_mode="HTML",
                            )
                        await asyncio.sleep(2)
                    except TelegramError as e:
                        logger.error(f"❌ Telegram error for {symbol}: {e}")
                    except Exception as e:
                        logger.error(f"❌ Error analyzing {symbol}: {e}")
                await asyncio.sleep(self.monitoring_interval)
            except Exception as e:
                logger.error(f"❌ Error in monitoring loop: {e}")
                await asyncio.sleep(60)

    def run(self) -> None:
        logger.info("=" * 70)
        logger.info("🚀 Starting Telegram Bot")
        logger.info("=" * 70)
        self.setup_handlers()
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot = CryptoSignalTelegramBot()
    bot.run()
