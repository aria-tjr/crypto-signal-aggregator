from aggregator import SignalFormatter
from datetime import datetime
import pytest

sample_result = {
    'symbol': 'BTC/USDT',
    'timestamp': datetime.now().isoformat(),
    'recommendation': 'BUY',
    'confidence_score': 0.85,
    'valid_sources': 9,
    'execution_time': 8.5,
    'bot_signals': {
        'technical_basic': {'signal': 1, 'confidence': 0.9},
        'technical_advanced': {'signal': 1, 'confidence': 0.85},
        'ml_prediction': {'signal': 1, 'confidence': 0.8},
        'onchain': {'signal': 1, 'confidence': 0.75},
        'sentiment': {'signal': 1, 'confidence': 0.8},
        'volume': {'signal': 0, 'confidence': 0.5},
        'volatility': {'signal': -1, 'confidence': 0.4},
        'correlation': {'signal': 1, 'confidence': 0.7},
        'macro': {'signal': 1, 'confidence': 0.8},
        'ai': {'signal': 1, 'confidence': 0.85},
    }
}

@pytest.mark.parametrize("rec", ["BUY", "SELL", "HOLD"])
def test_format_for_telegram_contains_key_fields(rec):
    formatter = SignalFormatter()
    sample = dict(sample_result)
    sample["recommendation"] = rec
    msg = formatter.format_for_telegram(sample)
    assert "BTC/USDT" in msg
    assert rec in msg
    assert "Confidence" in msg or "اعتماد" in msg

if __name__ == "__main__":
    # Manual run: print a sample
    formatter = SignalFormatter()
    print(formatter.format_for_telegram(sample_result))
