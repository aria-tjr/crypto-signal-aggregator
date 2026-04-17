"""
🔗 Signal Aggregator - ترکیب سیگنال‌های ۱۰ بات
- جمع‌آوری سیگنال‌ها به صورت Concurrent
- ترکیب وزن‌شده سیگنال‌ها
- محاسبه اعتماد نهایی
- تولید سیگنال نهایی
"""

from __future__ import annotations

import asyncio
import logging
from typing import Dict, List, Tuple
from datetime import datetime

from bots import (
    BasicTechnicalBot,
    AdvancedTechnicalBot,
    MLPredictionBot,
    OnChainAnalysisBot,
    SentimentAnalysisBot,
    VolumeAnalysisBot,
    VolatilityBot,
    CorrelationBot,
    MacroIndicatorsBot,
    AIAnalysisBot,
)

from config.settings import BOT_WEIGHTS, BOT_NAMES

logger = logging.getLogger(__name__)


class HybridSignalAggregator:
    """
    سیستم ترکیب سیگنال‌های ۱۰ بات تخصصی
    """

    def __init__(self) -> None:
        """اولیه‌سازی تمام بات‌ها"""

        logger.info("=" * 70)
        logger.info("🚀 Initializing HybridSignalAggregator with 10 bots")
        logger.info("=" * 70)

        self.bots: Dict[str, object] = {}
        self.bot_names_display: Dict[str, str] = BOT_NAMES
        self.weights: Dict[str, float] = BOT_WEIGHTS

        # ایجاد بات‌ها
        self._initialize_bots()

        # Statistics
        self.total_analyses: int = 0
        self.successful_analyses: int = 0

    def _initialize_bots(self) -> None:
        """اولیه‌سازی تمام ۱۰ بات"""

        bots_to_init = [
            ("technical_basic", BasicTechnicalBot),
            ("technical_advanced", AdvancedTechnicalBot),
            ("ml_prediction", MLPredictionBot),
            ("onchain", OnChainAnalysisBot),
            ("sentiment", SentimentAnalysisBot),
            ("volume", VolumeAnalysisBot),
            ("volatility", VolatilityBot),
            ("correlation", CorrelationBot),
            ("macro", MacroIndicatorsBot),
            ("ai", AIAnalysisBot),
        ]

        for bot_key, bot_class in bots_to_init:
            try:
                self.bots[bot_key] = bot_class()
                logger.info(f"   ✅ {self.bot_names_display[bot_key]} initialized")
            except Exception as e:
                logger.warning(f"   ⚠️  {self.bot_names_display.get(bot_key, bot_key)} failed: {e}")
                self.bots[bot_key] = None

        logger.info("=" * 70)

    async def aggregate_signals(self, symbol: str) -> Dict:
        """
        جمع‌آوری و ترکیب سیگنال‌های تمام بات‌ها
        """

        self.total_analyses += 1

        logger.info("")
        logger.info("🔍" * 35)
        logger.info(f"📊 Aggregating signals for {symbol}")
        logger.info("🔍" * 35)

        start_time = datetime.now()

        # ایجاد result dictionary
        result: Dict = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "start_time": start_time,
            "bot_signals": {},
            "aggregated_signal": 0.0,
            "confidence_score": 0.0,
            "recommendation": "HOLD",
            "valid_sources": 0,
            "failed_sources": 0,
            "analysis_details": [],
            "execution_time": 0.0,
        }

        # جمع‌آوری سیگنال‌ها به صورت Concurrent
        logger.info("📡 Fetching signals from all 10 bots concurrently...")

        try:
            # لیست کورتین‌ها برای concurrent execution
            coroutines = []
            bot_keys: List[str] = []

            for bot_key, bot_instance in self.bots.items():
                if bot_instance is not None:
                    coroutines.append(bot_instance.analyze(symbol))
                    bot_keys.append(bot_key)
                else:
                    result["failed_sources"] += 1

            # اجرای تمام بات‌ها به طور همزمان
            if coroutines:
                responses = await asyncio.gather(*coroutines, return_exceptions=True)

                # پردازش نتایج
                for bot_key, response in zip(bot_keys, responses):
                    self._process_bot_response(bot_key, response, result)

        except Exception as e:
            logger.error(f"❌ Critical error during signal aggregation: {e}")
            return result

        # محاسبه سیگنال نهایی
        logger.info("🧮 Computing final signal...")
        self._calculate_final_signal(result)

        # محاسبه زمان اجرا
        result["execution_time"] = (datetime.now() - start_time).total_seconds()

        # Log نتایج
        self._log_results(result)

        self.successful_analyses += 1

        return result

    def _process_bot_response(self, bot_key: str, response: object, result: Dict) -> None:
        """
        پردازش پاسخ هر بات
        """

        if isinstance(response, Exception):
            logger.warning(f"   ❌ {self.bot_names_display.get(bot_key, bot_key)}: {response}")
            result["bot_signals"][bot_key] = {
                "signal": 0,
                "confidence": 0,
                "error": str(response),
            }
            result["failed_sources"] += 1
            return

        if not isinstance(response, dict):
            logger.warning(
                f"   ❌ {self.bot_names_display.get(bot_key, bot_key)}: Invalid response format"
            )
            result["bot_signals"][bot_key] = {
                "signal": 0,
                "confidence": 0,
                "error": "Invalid format",
            }
            result["failed_sources"] += 1
            return

        # استخراج سیگنال و اعتماد
        signal = int(response.get("signal", 0))
        confidence = float(response.get("confidence", 0))

        # ذخیره سیگنال
        result["bot_signals"][bot_key] = {
            "signal": signal,
            "confidence": confidence,
            "raw_response": response,
        }

        # لاگ سیگنال
        signal_emoji = {1: "🟢", -1: "🔴", 0: "⚪"}.get(signal, "⚪")
        logger.info(
            f"   {signal_emoji} {self.bot_names_display.get(bot_key, bot_key)}: {signal:+d} ({confidence*100:.0f}%)"
        )

        # افزایش تعداد منابع موفق اگر سیگنال معتبر باشد
        if signal != 0:
            result["valid_sources"] += 1

    def _calculate_final_signal(self, result: Dict) -> None:
        """
        محاسبه سیگنال نهایی از ترکیب وزن‌شده
        """
        total_weighted_signal = 0.0
        total_weight_applied = 0.0
        signal_count = 0

        logger.info("\n📊 Weighted Signal Calculation:")
        logger.info("-" * 70)

        for bot_key, signal_data in result["bot_signals"].items():
            if "error" in signal_data:
                continue

            signal = int(signal_data["signal"])  # -1, 0, 1
            confidence = float(signal_data["confidence"])  # 0..1
            weight = float(self.weights.get(bot_key, 0.0))

            if signal != 0 and weight > 0:
                # محاسبه سیگنال وزن‌شده
                weighted_signal = signal * weight * confidence
                total_weighted_signal += weighted_signal
                total_weight_applied += (weight * confidence)
                signal_count += 1

                # لاگ محاسبه
                logger.info(
                    f"   {self.bot_names_display.get(bot_key, bot_key):25} | "
                    f"Signal: {signal:+2d} | "
                    f"Conf: {confidence:5.1%} | "
                    f"Weight: {weight:5.1%} | "
                    f"Weighted: {weighted_signal:+.4f}"
                )

        logger.info("-" * 70)

        # محاسبه نمره نهایی با آستانه پویا
        nonzero = sum(
            1
            for s in result["bot_signals"].values()
            if isinstance(s, dict) and s.get("signal", 0) != 0 and "error" not in s
        )
        required = max(3, int((nonzero * 0.6) + 0.999))  # ceil(0.6*nonzero), حداقل 3

        if signal_count >= required and nonzero > 0:
            if total_weight_applied > 0:
                final_weighted_signal = total_weighted_signal / total_weight_applied
                final_confidence = min(abs(final_weighted_signal) * (signal_count / 10), 1.0)
            else:
                final_weighted_signal = 0.0
                final_confidence = 0.0

            if final_weighted_signal > 0.15:
                recommendation = "BUY"
            elif final_weighted_signal < -0.15:
                recommendation = "SELL"
            else:
                recommendation = "HOLD"
        else:
            logger.warning(f"⚠️  Only {signal_count} bots agreed (need ≥{required})")
            if total_weight_applied > 0:
                final_weighted_signal = total_weighted_signal / total_weight_applied
                final_confidence = min(abs(final_weighted_signal) * (max(signal_count, 1) / 10), 0.5)
            else:
                final_weighted_signal = 0.0
                final_confidence = 0.0
            if final_weighted_signal > 0.25:
                recommendation = "BUY"
            elif final_weighted_signal < -0.25:
                recommendation = "SELL"
            else:
                recommendation = "HOLD"

        result["aggregated_signal"] = float(final_weighted_signal)
        result["confidence_score"] = float(final_confidence)
        result["recommendation"] = recommendation

        logger.info(f"\n✅ Final Result:")
        logger.info(f"   Aggregated Signal: {final_weighted_signal:+.4f}")
        logger.info(f"   Confidence Score: {final_confidence:.1%}")
        logger.info(f"   Recommendation: {recommendation}")
        logger.info(f"   Valid Sources: {signal_count}/10")

    def _log_results(self, result: Dict) -> None:
        """
        لاگ نتایج نهایی
        """

        emoji_map = {"BUY": "🟢🟢🟢", "SELL": "🔴🔴🔴", "HOLD": "⚪⚪⚪"}

        logger.info("")
        logger.info("=" * 70)
        logger.info(
            f"{emoji_map[result['recommendation']]} FINAL SIGNAL {emoji_map[result['recommendation']]}"
        )
        logger.info("=" * 70)
        logger.info(f"Symbol:           {result['symbol']}")
        logger.info(f"Recommendation:   {result['recommendation']}")
        logger.info(f"Confidence:       {result['confidence_score']:.1%}")
        logger.info(f"Valid Sources:    {result['valid_sources']}/10")
        logger.info(f"Failed Sources:   {result['failed_sources']}/10")
        logger.info(f"Execution Time:   {result['execution_time']:.2f} seconds")
        logger.info("=" * 70)
        logger.info("")

    def get_statistics(self) -> Dict:
        """
        دریافت آمار تجمیع
        """

        success_rate = (
            (self.successful_analyses / self.total_analyses * 100)
            if self.total_analyses > 0
            else 0
        )

        return {
            "total_analyses": self.total_analyses,
            "successful_analyses": self.successful_analyses,
            "success_rate": success_rate,
            "average_execution_time": "N/A",  # قابل بهبود
        }


# ===== Test Usage =====
if __name__ == "__main__":
    async def test_aggregator() -> None:
        logger.info("🧪 Testing HybridSignalAggregator...")

        aggregator = HybridSignalAggregator()
        result = await aggregator.aggregate_signals("BTC/USDT")

        print(f"\n📊 Result:")
        print(f"Symbol: {result['symbol']}")
        print(f"Recommendation: {result['recommendation']}")
        print(f"Confidence: {result['confidence_score']:.1%}")
        print(f"Valid Sources: {result['valid_sources']}/10")

    asyncio.run(test_aggregator())
