"""
📊 Confidence Scorer - محاسبه درجات اعتماد
"""

from __future__ import annotations

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


class ConfidenceScorer:
    """
    محاسبه امتیازات اعتماد برای سیگنال‌ها
    """

    @staticmethod
    def calculate_confidence(
        bot_signal: int,
        bot_confidence: float,
        bot_weight: float,
        aggregated_signal: float,
    ) -> float:
        """
        محاسبه اعتماد نهایی
        """

        if bot_signal == 0:
            return 0.0

        # اعتماد ترکیبی
        combined_confidence = bot_confidence * bot_weight

        # تعدیل بر اساس جهت‌مندی سیگنال جمع‌شده
        if (bot_signal > 0 and aggregated_signal > 0) or (
            bot_signal < 0 and aggregated_signal < 0
        ):
            # هم‌راستا = اعتماد بیشتر
            direction_boost = 1.1
        elif (bot_signal > 0 and aggregated_signal < 0) or (
            bot_signal < 0 and aggregated_signal > 0
        ):
            # مخالف = اعتماد کم‌تر
            direction_boost = 0.7
        else:
            direction_boost = 1.0

        final_confidence = min(combined_confidence * direction_boost, 1.0)

        return float(final_confidence)

    @staticmethod
    def calculate_agreement_level(bot_signals: Dict) -> Tuple[int, float]:
        """
        محاسبه سطح توافق بین بات‌ها

        Returns:
            (agreement_count, agreement_percentage)
        """

        total_signals = 0
        buy_signals = 0
        sell_signals = 0

        for _bot_key, signal_data in bot_signals.items():
            if "error" not in signal_data:
                signal = int(signal_data.get("signal", 0))

                if signal > 0:
                    buy_signals += 1
                    total_signals += 1
                elif signal < 0:
                    sell_signals += 1
                    total_signals += 1

        if total_signals == 0:
            return 0, 0.0

        max_agreement = max(buy_signals, sell_signals)
        agreement_percentage = (max_agreement / total_signals) * 100.0

        return max_agreement, float(agreement_percentage)

    @staticmethod
    def classify_confidence_level(confidence_score: float) -> str:
        """
        طبقه‌بندی سطح اعتماد
        """

        if confidence_score >= 0.90:
            return "VERY HIGH"
        elif confidence_score >= 0.75:
            return "HIGH"
        elif confidence_score >= 0.60:
            return "MEDIUM"
        elif confidence_score >= 0.40:
            return "LOW"
        else:
            return "VERY LOW"


# ===== Test =====
if __name__ == "__main__":
    scorer = ConfidenceScorer()

    confidence = scorer.calculate_confidence(
        bot_signal=1, bot_confidence=0.85, bot_weight=0.15, aggregated_signal=0.8
    )

    print(f"Confidence: {confidence:.1%}")
    print(f"Level: {scorer.classify_confidence_level(confidence)}")
