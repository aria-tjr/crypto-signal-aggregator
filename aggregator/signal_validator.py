"""
✅ Signal Validator - بررسی validity سیگنال‌ها
"""

from __future__ import annotations

import logging
from typing import Dict, Tuple, List

logger = logging.getLogger(__name__)


class SignalValidator:
    """
    بررسی کیفیت و اعتبار سیگنال‌های تولید شده
    """

    @staticmethod
    def is_valid_signal(result: Dict) -> Tuple[bool, str]:
        """
        بررسی اینکه سیگنال معتبر است یا نه
        """

        # معیار ۱: تعداد منابع موفق
        if result.get("valid_sources", 0) < 7:
            return False, f"Not enough valid sources ({result.get('valid_sources', 0)}/10)"

        # معیار ۲: نمره اعتماد
        if float(result.get("confidence_score", 0.0)) < 0.60:
            return False, f"Confidence too low ({float(result.get('confidence_score', 0.0)):.1%})"

        # معیار ۳: سیگنال نهایی
        if result.get("recommendation") == "HOLD":
            if float(result.get("confidence_score", 0.0)) < 0.75:
                return False, "HOLD signal with low confidence"

        # معیار ۴: سیگنال جمع‌شده
        aggregated_signal = float(result.get("aggregated_signal", 0.0))
        if abs(aggregated_signal) < 0.1:
            return False, "Aggregated signal too weak"

        return True, "Signal is valid"

    @staticmethod
    def filter_signals(results: List[Dict], min_confidence: float = 0.75) -> List[Dict]:
        """
        فیلتر کردن سیگنال‌های ضعیف
        """

        filtered: List[Dict] = []

        for result in results:
            is_valid, reason = SignalValidator.is_valid_signal(result)

            if is_valid and float(result.get("confidence_score", 0.0)) >= min_confidence:
                filtered.append(result)
            else:
                logger.debug(f"Filtered {result.get('symbol', '?')}: {reason}")

        return filtered

    @staticmethod
    def validate_bot_response(response: Dict) -> bool:
        """
        بررسی اینکه پاسخ بات درست فرمت است
        """

        required_fields = ["symbol", "signal", "confidence"]

        for field in required_fields:
            if field not in response:
                logger.warning(f"Missing field in bot response: {field}")
                return False

        if not isinstance(response["signal"], int) or response["signal"] not in [-1, 0, 1]:
            logger.warning(f"Invalid signal value: {response['signal']}")
            return False

        if not isinstance(response["confidence"], (int, float)) or not (
            0 <= float(response["confidence"]) <= 1
        ):
            logger.warning(f"Invalid confidence value: {response['confidence']}")
            return False

        return True
