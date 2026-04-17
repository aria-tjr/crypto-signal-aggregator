import asyncio
import logging
import pytest
from aggregator import HybridSignalAggregator

logging.basicConfig(level=logging.INFO)


@pytest.mark.asyncio
async def test_aggregation():
    print("\n🧪 Testing Signal Aggregation...\n")

    # ایجاد aggregator
    aggregator = HybridSignalAggregator()

    # تجمیع سیگنال‌ها
    result = await aggregator.aggregate_signals('BTC/USDT')

    # Assertions (basic sanity)
    assert isinstance(result, dict)
    assert result.get('symbol') == 'BTC/USDT'
    assert 'recommendation' in result
    assert 'confidence_score' in result
    assert 'valid_sources' in result

    # نمایش statistics
    stats = aggregator.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"   Total Analyses: {stats['total_analyses']}")
    print(f"   Success Rate: {stats['success_rate']:.1f}%")


if __name__ == "__main__":
    asyncio.run(test_aggregation())
