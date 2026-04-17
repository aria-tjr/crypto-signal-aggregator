"""
Wrapper برای Jesse Framework
استفاده از شاخص‌های پیشرفته
"""

from typing import Dict
import numpy as np
import ccxt
import asyncio
import logging
from datetime import datetime

# Optional TA-Lib with fallback to pure-python `ta`
try:  # pragma: no cover
    import talib as _talib  # type: ignore
except Exception:
    _talib = None  # type: ignore
    try:
        import pandas as _pd  # type: ignore
        import ta as _ta  # type: ignore
    except Exception:
        _pd = None  # type: ignore
        _ta = None  # type: ignore

logger = logging.getLogger(__name__)


class AdvancedTechnicalBot:
    """
    تکنیکال پیشرفته - استفاده از مجموعه شاخص‌های قوی‌تر
    """

    def __init__(self, exchange_name: str = 'binance'):
        try:
            self.exchange = getattr(ccxt, exchange_name)()
            logger.info("✅ AdvancedTechnicalBot initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing AdvancedTechnicalBot: {e}")
            raise

    async def analyze(self, symbol: str) -> Dict:
        """
        تحلیل شاخص‌های پیشرفته
        """
        logger.info(f"🔍 AdvancedTechnicalBot analyzing {symbol}")

        try:
            ohlcv = await asyncio.to_thread(self.exchange.fetch_ohlcv, symbol, '4h', None, 150, {})

            if not ohlcv or len(ohlcv) < 50:
                return {'symbol': symbol, 'signal': 0, 'confidence': 0}

            close = np.array([x[4] for x in ohlcv], dtype=np.float64)
            high = np.array([x[2] for x in ohlcv], dtype=np.float64)
            low = np.array([x[3] for x in ohlcv], dtype=np.float64)

            # شاخص‌های پیشرفته (TA-Lib → ta)
            if _talib is not None:
                adx = _talib.ADX(high, low, close, 14)
                plus_di = _talib.PLUS_DI(high, low, close, 14)
                minus_di = _talib.MINUS_DI(high, low, close, 14)
                atr = _talib.ATR(high, low, close, 14)
                k, d = _talib.STOCH(high, low, close)
                adx_val = float(adx[-1])
                plus_val = float(plus_di[-1])
                minus_val = float(minus_di[-1])
                atr_val = float(atr[-1])
                k_val = float(k[-1])
            elif _ta is not None and _pd is not None:
                s_close = _pd.Series(close)
                s_high = _pd.Series(high)
                s_low = _pd.Series(low)
                adx_ind = _ta.trend.ADXIndicator(high=s_high, low=s_low, close=s_close, window=14)
                adx_val = float(adx_ind.adx().iloc[-1])
                plus_val = float(adx_ind.adx_pos().iloc[-1])
                minus_val = float(adx_ind.adx_neg().iloc[-1])
                atr_val = float(_ta.volatility.AverageTrueRange(high=s_high, low=s_low, close=s_close, window=14).average_true_range().iloc[-1])
                stoch = _ta.momentum.StochasticOscillator(high=s_high, low=s_low, close=s_close)
                k_val = float(stoch.stoch().iloc[-1])
            else:
                raise RuntimeError("No technical analysis backend available (talib/ta)")

            # سیگنال
            signal_count = 0

            if adx_val > 25:  # Trend قوی
                if plus_val > minus_val:
                    signal_count += 1  # Uptrend
                else:
                    signal_count -= 1  # Downtrend

            if k_val < 20:
                signal_count += 1
            elif k_val > 80:
                signal_count -= 1

            signal = 0
            if signal_count >= 1:
                signal = 1
            elif signal_count <= -1:
                signal = -1

            confidence = min(abs(signal_count) / 2, 1.0)

            return {
                'symbol': symbol,
                'signal': signal,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'indicators': {
                    'adx': float(adx_val),
                    'plus_di': float(plus_val),
                    'minus_di': float(minus_val),
                    'atr_percent': (float(atr_val) / float(close[-1])) * 100
                }
            }

        except Exception as e:
            logger.error(f"❌ AdvancedTechnicalBot error analyzing {symbol}: {e}")
            return {'symbol': symbol, 'signal': 0, 'confidence': 0}
