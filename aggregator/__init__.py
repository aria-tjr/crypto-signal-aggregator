"""
Aggregator Module - ترکیب و جمع‌آوری سیگنال‌ها
"""

import logging

logger = logging.getLogger(__name__)

try:
    from .signal_aggregator import HybridSignalAggregator
    logger.info("✅ HybridSignalAggregator loaded")
except Exception as e:
    logger.error(f"❌ Error loading HybridSignalAggregator: {e}")

try:
    from .confidence_scorer import ConfidenceScorer
    logger.info("✅ ConfidenceScorer loaded")
except Exception as e:
    logger.error(f"❌ Error loading ConfidenceScorer: {e}")

try:
    from .signal_formatter import SignalFormatter
    logger.info("✅ SignalFormatter loaded")
except Exception as e:
    logger.error(f"❌ Error loading SignalFormatter: {e}")

try:
    from .signal_validator import SignalValidator
    logger.info("✅ SignalValidator loaded")
except Exception as e:
    logger.error(f"❌ Error loading SignalValidator: {e}")

__all__ = [
    "HybridSignalAggregator",
    "ConfidenceScorer",
    "SignalFormatter",
    "SignalValidator",
]
