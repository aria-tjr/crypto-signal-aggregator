"""
Macro Indicators Bot (ساده)
"""

from typing import Dict
import logging

logger = logging.getLogger(__name__)


class MacroIndicatorsBot:
    async def analyze(self, symbol: str) -> Dict:
        """شاخص‌های کلان‌اقتصادی (Placeholder)"""
        logger.info(f"🔍 MacroIndicatorsBot analyzing {symbol}")
        return {'symbol': symbol, 'signal': 0, 'confidence': 0.5}
