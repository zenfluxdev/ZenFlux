"""Shared fixtures for ZenFlux tests."""

import pytest
from zenflux.models import MarketSnapshot


def make_snap(
    symbol="BTC",
    timestamp=1700000000.0,
    realized_vol_1d=60.0,
    realized_vol_7d=65.0,
    realized_vol_30d=70.0,
    bid_ask_spread_pct=0.08,
    bid_ask_spread_7d_avg=0.08,
    orderbook_depth_usd=15_000_000.0,
    orderbook_depth_7d_avg=15_000_000.0,
    price=42_000.0,
    ma_7d=42_000.0,
    ma_30d=40_000.0,
    price_high_30d=48_000.0,
    price_low_30d=36_000.0,
    buy_volume_1h=5_000_000.0,
    sell_volume_1h=5_000_000.0,
    buy_volume_24h=120_000_000.0,
    sell_volume_24h=120_000_000.0,
    correlation_7d=0.82,
    correlation_30d=0.80,
) -> MarketSnapshot:
    return MarketSnapshot(
        symbol=symbol, timestamp=timestamp,
        realized_vol_1d=realized_vol_1d, realized_vol_7d=realized_vol_7d,
        realized_vol_30d=realized_vol_30d,
        bid_ask_spread_pct=bid_ask_spread_pct, bid_ask_spread_7d_avg=bid_ask_spread_7d_avg,
        orderbook_depth_usd=orderbook_depth_usd, orderbook_depth_7d_avg=orderbook_depth_7d_avg,
        price=price, ma_7d=ma_7d, ma_30d=ma_30d,
        price_high_30d=price_high_30d, price_low_30d=price_low_30d,
        buy_volume_1h=buy_volume_1h, sell_volume_1h=sell_volume_1h,
        buy_volume_24h=buy_volume_24h, sell_volume_24h=sell_volume_24h,
        correlation_7d=correlation_7d, correlation_30d=correlation_30d,
    )


@pytest.fixture
def neutral_snap():
    return make_snap()


@pytest.fixture
def calm_snap():
    return make_snap(
        realized_vol_1d=30.0, realized_vol_7d=35.0, realized_vol_30d=60.0,
        bid_ask_spread_pct=0.04, bid_ask_spread_7d_avg=0.08,
        orderbook_depth_usd=22_000_000.0, orderbook_depth_7d_avg=15_000_000.0,
        price=42_500.0, ma_7d=42_200.0, ma_30d=41_000.0,
        price_high_30d=48_000.0, price_low_30d=36_000.0,
        buy_volume_1h=5_100_000.0, sell_volume_1h=4_900_000.0,
        buy_volume_24h=122_000_000.0, sell_volume_24h=118_000_000.0,
        correlation_7d=0.88, correlation_30d=0.85,
    )


@pytest.fixture
def stress_snap():
    return make_snap(
        realized_vol_1d=180.0, realized_vol_7d=130.0, realized_vol_30d=70.0,
        bid_ask_spread_pct=0.45, bid_ask_spread_7d_avg=0.08,
        orderbook_depth_usd=4_000_000.0, orderbook_depth_7d_avg=15_000_000.0,
        price=38_000.0, ma_7d=44_000.0, ma_30d=43_000.0,
        price_high_30d=48_000.0, price_low_30d=36_500.0,
        buy_volume_1h=1_000_000.0, sell_volume_1h=9_000_000.0,
        buy_volume_24h=60_000_000.0, sell_volume_24h=180_000_000.0,
        correlation_7d=0.15, correlation_30d=0.80,
    )
