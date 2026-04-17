"""
Volume Analysis Bot (ساده اما کاربردی)

سیگنال بر اساس رشد حجم نسبت به میانگین 20 کندل اخیر.
"""

from typing import Dict
import logging
import asyncio
import ccxt
import numpy as np

logger = logging.getLogger(__name__)


class VolumeAnalysisBot:
    def __init__(self, exchange_name: str = 'binance') -> None:
        self.exchange = getattr(ccxt, exchange_name)()

    async def analyze(self, symbol: str) -> Dict:
        """تحلیل حجم: اگر حجم آخر > 1.3 * SMA20 → BUY، اگر < 0.7 * SMA20 → SELL"""
        logger.info(f"🔍 VolumeAnalysisBot analyzing {symbol}")
        try:
            ohlcv = await asyncio.to_thread(self.exchange.fetch_ohlcv, symbol, '1h', None, 50, {})
            if not ohlcv or len(ohlcv) < 21:
                return {'symbol': symbol, 'signal': 0, 'confidence': 0.4}

            volumes = np.array([x[5] for x in ohlcv], dtype=float)
            v_last = float(volumes[-1])
            sma20 = float(np.mean(volumes[-21:-1]))
            if sma20 <= 0:
                return {'symbol': symbol, 'signal': 0, 'confidence': 0.4}

            ratio = v_last / sma20
            if ratio > 1.3:
                signal = 1
            elif ratio < 0.7:
                signal = -1
            else:
                signal = 0

            confidence = min(abs(ratio - 1.0), 1.0)
            return {'symbol': symbol, 'signal': signal, 'confidence': confidence}
        except Exception as e:
            logger.warning(f"❌ VolumeAnalysisBot error: {e}")
            return {'symbol': symbol, 'signal': 0, 'confidence': 0.4, 'error': str(e)}
