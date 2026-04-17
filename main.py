"""
🚀 Main Entry Point - نقطه شروع سیستم
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Crypto Signal Telegram Bot
بات تلگرام برای تولید سیگنال معاملات فیوچرز
با ۱۰ منبع تحلیلی تخصصی

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from __future__ import annotations

import asyncio
import signal
import logging
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Add project root to path (for direct execution)
PROJECT_ROOT = Path(__file__).parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tg_bot import CryptoSignalTelegramBot
from telegram import Update  # type: ignore
from utils.logger import setup_logger
from config.settings import validate_settings

# Optional lightweight HTTP health endpoint
try:
    from aiohttp import web
except Exception:  # pragma: no cover - only used when available
    web = None  # type: ignore

# Setup main logger
main_logger = setup_logger("CryptoSignalBot")


class CryptoSignalBotSystem:
    """
    سیستم کامل بات سیگنال معاملات
    - مدیریت lifecycle
    - Error handling
    - Health checks
    - Graceful shutdown
    """

    def __init__(self) -> None:
        """اولیه‌سازی سیستم"""

        self.logger = main_logger
        self.bot: Optional[CryptoSignalTelegramBot] = None
        self.is_running: bool = False

        # Health server (aiohttp)
        self._web_app: Optional[web.Application] = None if web else None  # type: ignore
        self._web_runner: Optional[web.AppRunner] = None if web else None  # type: ignore
        self._web_site: Optional[web.BaseSite] = None if web else None  # type: ignore

        self.logger.info("=" * 80)
        self.logger.info("🚀 Initializing Crypto Signal Bot System")
        self.logger.info("=" * 80)

    def validate_environment(self) -> bool:
        """بررسی تنظیمات محیطی"""

        self.logger.info("\n📋 Validating environment...")

        try:
            # بارگذاری .env
            load_dotenv()
            self.logger.info("   ✅ .env file loaded")

            # بررسی settings
            validate_settings()
            self.logger.info("   ✅ Settings validated")

            # بررسی پوشه‌های مهم
            required_dirs = ["logs", "data"]
            for dir_name in required_dirs:
                dir_path = PROJECT_ROOT / dir_name
                if not dir_path.exists():
                    dir_path.mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"   ✅ Created directory: {dir_name}")

            self.logger.info("✅ Environment validation passed\n")
            return True

        except ValueError as e:
            self.logger.error(f"❌ Validation error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Unexpected error during validation: {e}")
            return False

    async def initialize_bot(self) -> bool:
        """اولیه‌سازی بات تلگرام"""

        self.logger.info("🤖 Initializing Telegram Bot...")

        try:
            self.bot = CryptoSignalTelegramBot()
            self.logger.info("✅ Telegram Bot initialized successfully\n")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error initializing bot: {e}")
            return False

    async def _start_health_server(self) -> None:
        """Start a tiny HTTP health server if aiohttp is available."""

        if web is None:
            self.logger.info("ℹ️ aiohttp not installed — skipping /health endpoint")
            return

        async def health(_: web.Request) -> web.Response:  # type: ignore
            data = {
                "status": "ok",
                "running": self.is_running,
                "bot": bool(self.bot),
            }
            return web.json_response(data)

        if self._web_app is None:
            self._web_app = web.Application()
            self._web_app.router.add_get("/health", health)
            self._web_runner = web.AppRunner(self._web_app)
            await self._web_runner.setup()
            self._web_site = web.TCPSite(self._web_runner, host="0.0.0.0", port=8000)
            await self._web_site.start()
            self.logger.info("🩺 Health endpoint started on http://0.0.0.0:8000/health")

    async def _stop_health_server(self) -> None:
        """Stop HTTP health server if running."""
        if web is None:
            return
        try:
            if self._web_site:
                await self._web_site.stop()  # type: ignore
            if self._web_runner:
                await self._web_runner.cleanup()  # type: ignore
        except Exception as e:
            self.logger.warning(f"⚠️ Error stopping health server: {e}")
        finally:
            self._web_site = None
            self._web_runner = None
            self._web_app = None

    async def run(self) -> bool:
        """اجرای سیستم"""

        # بررسی محیط
        if not self.validate_environment():
            self.logger.error("❌ Environment validation failed")
            return False

        # اولیه‌سازی بات
        if not await self.initialize_bot():
            self.logger.error("❌ Bot initialization failed")
            return False

        # Start health endpoint (non-fatal if unavailable)
        await self._start_health_server()

        # شروع بات
        self.is_running = True

        self.logger.info("=" * 80)
        self.logger.info("🎯 Bot is running and ready for commands")
        self.logger.info("=" * 80)
        self.logger.info("")
        self.logger.info("📲 Available Commands:")
        self.logger.info("   /start   - Welcome message")
        self.logger.info("   /signal  - Generate signal for a coin")
        self.logger.info("   /monitor - Start automatic monitoring")
        self.logger.info("   /stop    - Stop monitoring")
        self.logger.info("   /add     - Add coin to monitoring list")
        self.logger.info("   /remove  - Remove coin from monitoring list")
        self.logger.info("   /list    - Show monitoring list")
        self.logger.info("   /status  - Show system status")
        self.logger.info("   /help    - Show help")
        self.logger.info("")
        self.logger.info("=" * 80)
        self.logger.info("")

        try:
            assert self.bot is not None
            # Configure handlers then start Application asynchronously
            self.bot.setup_handlers()
            app = self.bot.application  # type: ignore[union-attr]
            await app.initialize()
            await app.start()
            if hasattr(app, "updater") and hasattr(app.updater, "start_polling"):
                await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)

            stop_event = asyncio.Event()

            # Register signal handlers to trigger graceful shutdown
            try:
                loop = asyncio.get_running_loop()
                loop.add_signal_handler(signal.SIGINT, stop_event.set)
                loop.add_signal_handler(signal.SIGTERM, stop_event.set)
            except NotImplementedError:
                # Signals may not be available on some platforms
                pass
            try:
                await stop_event.wait()  # Wait until cancelled (Ctrl+C) or shutdown() toggles state
            except asyncio.CancelledError:
                # Expected on Ctrl+C when running under asyncio.run
                pass
            return True

        except KeyboardInterrupt:
            self.logger.info("\n⛔ Bot interrupted by user (Ctrl+C)")
            return False

        except Exception as e:
            self.logger.error(f"❌ Critical error: {e}", exc_info=True)
            return False
        finally:
            await self.shutdown()

    def _run_bot_in_thread(self) -> None:
        """Start the Telegram bot in a background thread with an event loop.

        PTB's run_polling expects an event loop to be available in the current thread.
        """
        import asyncio as _aio

        try:
            loop = _aio.new_event_loop()
            _aio.set_event_loop(loop)
            self.bot.run()  # type: ignore[union-attr]
        finally:
            try:
                loop = _aio.get_event_loop()
                loop.stop()
                loop.close()
            except Exception:
                pass

    async def shutdown(self) -> None:
        """إيقاف النظام بشكل آمن"""

        self.logger.info("")
        self.logger.info("=" * 80)
        self.logger.info("🛑 Shutting down bot system...")
        self.logger.info("=" * 80)

        try:
            # Try to gracefully stop PTB Application if accessible
            if self.bot and getattr(self.bot, "application", None) is not None:
                app = self.bot.application  # type: ignore[attr-defined]
                try:
                    # stop/shutdown are async in PTB v20+
                    if hasattr(app, "stop"):
                        await app.stop()  # type: ignore[func-returns-value]
                    if hasattr(app, "shutdown"):
                        await app.shutdown()
                except Exception as e:
                    self.logger.warning(f"⚠️ Error stopping Telegram application: {e}")

            self.is_running = False

            # Stop PTB application if running
            if self.bot and getattr(self.bot, "application", None) is not None:
                app = self.bot.application  # type: ignore[attr-defined]
                try:
                    if hasattr(app, "updater") and hasattr(app.updater, "stop"):
                        await app.updater.stop()
                    if hasattr(app, "stop"):
                        await app.stop()
                    if hasattr(app, "shutdown"):
                        await app.shutdown()
                except Exception as e:
                    self.logger.warning(f"⚠️ Error stopping Telegram application: {e}")

            # Stop health endpoint
            await self._stop_health_server()

            self.logger.info("✅ System shutdown complete")
            self.logger.info("=" * 80)

        except Exception as e:
            self.logger.error(f"❌ Error during shutdown: {e}")

    async def health_check(self) -> bool:
        """بررسی سلامت سیستم"""

        self.logger.info("🏥 Performing health check...")

        checks = {
            "Bot Status": self.bot is not None,
            "Running": self.is_running,
            "Aggregator": bool(getattr(self.bot, "aggregator", None)) if self.bot else False,
            "Telegram Connection": True,  # اگر بات اجرا می‌شود، connected است (approx.)
        }

        all_healthy = True

        for check_name, status in checks.items():
            status_emoji = "✅" if status else "❌"
            self.logger.info(f"   {status_emoji} {check_name}: {status}")
            if not status:
                all_healthy = False

        return all_healthy


async def main() -> None:
    """
    نقطه شروع اصلی برنامه
    """

    # ایجاد سیستم
    system = CryptoSignalBotSystem()

    try:
        # اجرای سیستم
        success = await system.run()

        if not success:
            sys.exit(1)

    except KeyboardInterrupt:
        await system.shutdown()
        sys.exit(0)

    except Exception as e:
        system.logger.error(f"❌ Fatal error: {e}", exc_info=True)
        await system.shutdown()
        sys.exit(1)


if __name__ == "__main__":
    # اجرای برنامه
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⛔ Bot stopped")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
