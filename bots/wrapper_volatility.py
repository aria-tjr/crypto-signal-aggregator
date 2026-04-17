"""
Volatility Analysis Bot (ساده)

سیگنال بر اساس تغییرات قیمت و پهنای باند ساده (انحراف معیار 20 کندل).
"""

from typing import Dict
import logging
import asyncio
import ccxt
import numpy as np

logger = logging.getLogger(__name__)


class VolatilityBot:
    def __init__(self, exchange_name: str = 'binance') -> None:
        self.exchange = getattr(ccxt, exchange_name)()

    async def analyze(self, symbol: str) -> Dict:
        """اگر بازه نوسان (۲*std20) بالا و کندل آخر سبز → BUY؛ بالا و کندل آخر قرمز → SELL"""
        logger.info(f"🔍 VolatilityBot analyzing {symbol}")
        try:
            ohlcv = await asyncio.to_thread(self.exchange.fetch_ohlcv, symbol, '1h', None, 60, {})
            if not ohlcv or len(ohlcv) < 21:
                return {'symbol': symbol, 'signal': 0, 'confidence': 0.4}

            closes = np.array([x[4] for x in ohlcv], dtype=float)
            opens = np.array([x[1] for x in ohlcv], dtype=float)
            ret = np.diff(closes) / closes[:-1]
            std20 = float(np.std(ret[-20:])) if len(ret) >= 20 else float(np.std(ret))
            band_width = 2.0 * std20
            last_green = closes[-1] > opens[-1]

            # Thresholds tuned lightly
            if band_width > 0.01:  # 1% band size
                signal = 1 if last_green else -1
                confidence = min(band_width * 10.0, 1.0)
            else:
                signal = 0
                confidence = band_width * 10.0

            return {'symbol': symbol, 'signal': signal, 'confidence': confidence}
        except Exception as e:
            logger.warning(f"❌ VolatilityBot error: {e}")
            return {'symbol': symbol, 'signal': 0, 'confidence': 0.4, 'error': str(e)}
