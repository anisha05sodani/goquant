import pytest
from datetime import datetime
from src.core.orderbook_processor import OrderBookProcessor, OrderBook

@pytest.fixture
def sample_orderbook_data():
    return {
        "timestamp": "2024-03-20T10:00:00Z",
        "exchange": "OKX",
        "symbol": "BTC-USDT-SWAP",
        "asks": [
            ["50000.0", "1.0"],
            ["50001.0", "2.0"]
        ],
        "bids": [
            ["49999.0", "1.5"],
            ["49998.0", "2.5"]
        ]
    }

@pytest.fixture
def processor():
    return OrderBookProcessor()

def test_process_message(processor, sample_orderbook_data):
    orderbook = processor.process_message(sample_orderbook_data)
    
    assert isinstance(orderbook, OrderBook)
    assert orderbook.exchange == "OKX"
    assert orderbook.symbol == "BTC-USDT-SWAP"
    assert len(orderbook.asks) == 2
    assert len(orderbook.bids) == 2
    assert orderbook.asks[0].price == 50000.0
    assert orderbook.asks[0].quantity == 1.0

def test_calculate_mid_price(processor, sample_orderbook_data):
    orderbook = processor.process_message(sample_orderbook_data)
    mid_price = processor.calculate_mid_price()
    
    expected_mid = (50000.0 + 49999.0) / 2
    assert mid_price == expected_mid 