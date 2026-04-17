"""
بات‌های تحلیلی - کلون شده از GitHub
۱۰ بات تخصصی برای تحلیل معاملات فیوچرز
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class NullBot:
	"""Fallback bot used when a real bot cannot be imported due to missing deps.

	Returns a neutral signal and logs the reason.
	"""

	def __init__(self, reason: str = "dependency missing") -> None:
		self.reason = reason

	async def analyze(self, symbol: str):  # pragma: no cover - simple fallback
		logger.warning(f"⚠️  Using NullBot for {self.__class__.__name__} ({self.reason})")
		return {"signal": 0, "confidence": 0.0, "error": self.reason}


def _fallback(name: str, reason: str):
	logger.error(f"❌ Error loading {name}: {reason}")
	# Create a distinct subclass so names remain meaningful
	return type(name, (NullBot,), {})


# Import all bots with resilient fallbacks
try:
	from .wrapper_technical_basic import BasicTechnicalBot  # type: ignore
	logger.info("✅ BasicTechnicalBot loaded")
except Exception as e:
	BasicTechnicalBot = _fallback("BasicTechnicalBot", str(e))  # type: ignore

try:
	from .wrapper_technical_advanced import AdvancedTechnicalBot  # type: ignore
	logger.info("✅ AdvancedTechnicalBot loaded")
except Exception as e:
	AdvancedTechnicalBot = _fallback("AdvancedTechnicalBot", str(e))  # type: ignore

try:
	from .wrapper_ml_prediction import MLPredictionBot  # type: ignore
	logger.info("✅ MLPredictionBot loaded")
except Exception as e:
	MLPredictionBot = _fallback("MLPredictionBot", str(e))  # type: ignore

try:
	from .wrapper_onchain import OnChainAnalysisBot  # type: ignore
	logger.info("✅ OnChainAnalysisBot loaded")
except Exception as e:
	OnChainAnalysisBot = _fallback("OnChainAnalysisBot", str(e))  # type: ignore

try:
	from .wrapper_sentiment import SentimentAnalysisBot  # type: ignore
	logger.info("✅ SentimentAnalysisBot loaded")
except Exception as e:
	SentimentAnalysisBot = _fallback("SentimentAnalysisBot", str(e))  # type: ignore

try:
	from .wrapper_volume import VolumeAnalysisBot  # type: ignore
	logger.info("✅ VolumeAnalysisBot loaded")
except Exception as e:
	VolumeAnalysisBot = _fallback("VolumeAnalysisBot", str(e))  # type: ignore

try:
	from .wrapper_volatility import VolatilityBot  # type: ignore
	logger.info("✅ VolatilityBot loaded")
except Exception as e:
	VolatilityBot = _fallback("VolatilityBot", str(e))  # type: ignore

try:
	from .wrapper_correlation import CorrelationBot  # type: ignore
	logger.info("✅ CorrelationBot loaded")
except Exception as e:
	CorrelationBot = _fallback("CorrelationBot", str(e))  # type: ignore

try:
	from .wrapper_macro import MacroIndicatorsBot  # type: ignore
	logger.info("✅ MacroIndicatorsBot loaded")
except Exception as e:
	MacroIndicatorsBot = _fallback("MacroIndicatorsBot", str(e))  # type: ignore

try:
	from .wrapper_ai import AIAnalysisBot  # type: ignore
	logger.info("✅ AIAnalysisBot loaded")
except Exception as e:
	AIAnalysisBot = _fallback("AIAnalysisBot", str(e))  # type: ignore

__all__ = [
	"BasicTechnicalBot",
	"AdvancedTechnicalBot",
	"MLPredictionBot",
	"OnChainAnalysisBot",
	"SentimentAnalysisBot",
	"VolumeAnalysisBot",
	"VolatilityBot",
	"CorrelationBot",
	"MacroIndicatorsBot",
	"AIAnalysisBot",
]
