"""
Wrapper برای Crypto-Signal
استفاده از کد موجود از GitHub (نسخه ساده)
"""

from typing import Dict
import numpy as np
import ccxt
import asyncio
import logging
from datetime import datetime

# Optional TA-Lib (native). Fallback to pure-python `ta` if unavailable.
try:  # pragma: no cover - import guard
    import talib as _talib  # type: ignore
except Exception:  # pragma: no cover - handled at runtime
    _talib = None  # type: ignore
    try:
        import pandas as _pd  # type: ignore
        import ta as _ta  # type: ignore
    except Exception:  # If even pure-python TA is missing, we'll handle below
        _pd = None  # type: ignore
        _ta = None  # type: ignore

logger = logging.getLogger(__name__)


class BasicTechnicalBot:
    """
    تکنیکال پایه - استفاده از شاخص‌های عمومی مشابه Crypto-Signal
    """

    def __init__(self, exchange_name: str = 'binance'):
        try:
            self.exchange = getattr(ccxt, exchange_name)()
            self.exchange_name = exchange_name
            logger.info("✅ BasicTechnicalBot initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing BasicTechnicalBot: {e}")
            raise

    async def analyze(self, symbol: str) -> Dict:
        """
        تحلیل سکه با شاخص‌های پایه
        خروجی: Dict با کلیدهای symbol, signal, confidence, indicators, timestamp
        """
        logger.info(f"🔍 BasicTechnicalBot analyzing {symbol}")

        try:
            # دریافت داده‌ها (در ترد جدا برای سازگاری با async)
            ohlcv = await asyncio.to_thread(self.exchange.fetch_ohlcv, symbol, '1h', None, 150, {})

            if not ohlcv or len(ohlcv) < 50:
                return {'symbol': symbol, 'signal': 0, 'confidence': 0}

            close = np.array([x[4] for x in ohlcv], dtype=np.float64)
            high = np.array([x[2] for x in ohlcv], dtype=np.float64)
            low = np.array([x[3] for x in ohlcv], dtype=np.float64)

            # شاخص‌ها (اولویت: TA-Lib → ta)
            if _talib is not None:
                ema9_arr = _talib.EMA(close, 9)
                ema21_arr = _talib.EMA(close, 21)
                rsi_arr = _talib.RSI(close, 14)
                macd, macd_signal, macd_hist = _talib.MACD(close)
                ema9_val = float(ema9_arr[-1])
                ema21_val = float(ema21_arr[-1])
                rsi_val = float(rsi_arr[-1])
                macd_val = float(macd[-1])
                macd_sig = float(macd_signal[-1])
            elif _ta is not None and _pd is not None:
                s_close = _pd.Series(close)
                ema9_series = _ta.trend.EMAIndicator(close=s_close, window=9).ema_indicator()
                ema21_series = _ta.trend.EMAIndicator(close=s_close, window=21).ema_indicator()
                rsi_series = _ta.momentum.RSIIndicator(close=s_close, window=14).rsi()
                macd_obj = _ta.trend.MACD(close=s_close)
                ema9_val = float(ema9_series.iloc[-1])
                ema21_val = float(ema21_series.iloc[-1])
                rsi_val = float(rsi_series.iloc[-1])
                macd_val = float(macd_obj.macd().iloc[-1])
                macd_sig = float(macd_obj.macd_signal().iloc[-1])
            else:
                raise RuntimeError("No technical analysis backend available (talib/ta)")

            # تولید سیگنال ساده
            signal_count = 0
            if ema9_val > ema21_val:
                signal_count += 1
            else:
                signal_count -= 1

            if rsi_val < 40:
                signal_count += 1
            elif rsi_val > 60:
                signal_count -= 1

            if macd_val > macd_sig:
                signal_count += 1
            else:
                signal_count -= 1

            signal = 0
            if signal_count >= 2:
                signal = 1
            elif signal_count <= -2:
                signal = -1

            confidence = min(abs(signal_count) / 3, 1.0)

            return {
                'symbol': symbol,
                'signal': signal,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'indicators': {
                    'ema9': float(ema9_val),
                    'ema21': float(ema21_val),
                    'rsi': float(rsi_val),
                    'macd': float(macd_val)
                }
            }

        except Exception as e:
            logger.error(f"❌ BasicTechnicalBot error analyzing {symbol}: {e}")
            return {'symbol': symbol, 'signal': 0, 'confidence': 0}
