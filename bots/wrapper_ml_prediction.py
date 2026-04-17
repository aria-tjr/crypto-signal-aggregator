"""
Wrapper برای Freqtrade ML (ساده‌شده)
استفاده از پیش‌بینی قیمت با رگرسیون خطی
"""

from typing import Dict
import numpy as np
import ccxt
import asyncio
import logging
from datetime import datetime
from sklearn.linear_model import LinearRegression

logger = logging.getLogger(__name__)


class MLPredictionBot:
    """
    پیش‌بینی قیمت - استفاده از ML Models ساده
    """

    def __init__(self, exchange_name: str = 'binance'):
        try:
            self.exchange = getattr(ccxt, exchange_name)()
            self.model = LinearRegression()
            logger.info("✅ MLPredictionBot initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing MLPredictionBot: {e}")
            raise

    async def analyze(self, symbol: str) -> Dict:
        """
        پیش‌بینی قیمت
        """
        logger.info(f"🔍 MLPredictionBot analyzing {symbol}")

        try:
            ohlcv = await asyncio.to_thread(self.exchange.fetch_ohlcv, symbol, '1h', None, 300, {})

            if not ohlcv or len(ohlcv) < 100:
                return {'symbol': symbol, 'signal': 0, 'confidence': 0}

            close = np.array([x[4] for x in ohlcv], dtype=np.float64)

            # ساخت features
            X = []
            y = []

            for i in range(50, len(close) - 1):
                window = close[i-50:i]
                features = [
                    close[i],
                    float(np.mean(window)),
                    float(np.std(window)),
                    float((close[i] - close[i-10]) / close[i-10]) if close[i-10] != 0 else 0.0,
                ]
                X.append(features)
                y.append(close[i+1])

            X = np.array(X)
            y = np.array(y)

            if len(X) < 10:
                return {'symbol': symbol, 'signal': 0, 'confidence': 0}

            # Train
            self.model.fit(X, y)

            # Predict
            last_features = np.array([X[-1]])
            predicted = float(self.model.predict(last_features)[0])

            current = float(close[-1])
            change = ((predicted - current) / current) * 100 if current != 0 else 0.0

            signal = 1 if change > 0.5 else (-1 if change < -0.5 else 0)
            confidence = min(abs(change) / 2, 1.0)

            return {
                'symbol': symbol,
                'signal': signal,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'predictions': {
                    'current': current,
                    'predicted': predicted,
                    'change_pct': change
                }
            }

        except Exception as e:
            logger.error(f"❌ Error analyzing {symbol}: {e}")
            return {'symbol': symbol, 'signal': 0, 'confidence': 0}
