from dataclasses import dataclass
from typing import List, Tuple
from datetime import datetime

@dataclass
class OrderBookLevel:
    price: float
    quantity: float

@dataclass
class OrderBook:
    timestamp: datetime
    exchange: str
    symbol: str
    asks: List[OrderBookLevel]
    bids: List[OrderBookLevel]
    
    @property
    def mid_price(self) -> float:
        """Calculate mid price"""
        if not self.asks or not self.bids:
            return 0.0
        return (self.asks[0].price + self.bids[0].price) / 2
    
    @property
    def spread(self) -> float:
        """Calculate spread"""
        if not self.asks or not self.bids:
            return 0.0
        return self.asks[0].price - self.bids[0].price
    
    @property
    def depth(self) -> float:
        """Calculate orderbook depth"""
        ask_depth = sum(level.quantity for level in self.asks)
        bid_depth = sum(level.quantity for level in self.bids)
        return (ask_depth + bid_depth) / 2
    
    @property
    def total_volume(self) -> float:
        """Calculate total volume"""
        return sum(level.quantity for level in self.asks + self.bids)

class OrderBookProcessor:
    def __init__(self):
        self.current_orderbook: OrderBook = None
    
    def process_message(self, message: dict) -> OrderBook:
        """Process incoming WebSocket message into OrderBook format"""
        timestamp = datetime.fromisoformat(message["timestamp"].replace("Z", "+00:00"))
        
        asks = [
            OrderBookLevel(float(price), float(qty))
            for price, qty in message["asks"]
        ]
        
        bids = [
            OrderBookLevel(float(price), float(qty))
            for price, qty in message["bids"]
        ]
        
        self.current_orderbook = OrderBook(
            timestamp=timestamp,
            exchange=message["exchange"],
            symbol=message["symbol"],
            asks=asks,
            bids=bids
        )
        
        return self.current_orderbook

    def calculate_mid_price(self) -> float:
        """Calculate the current mid price."""
        if not self.current_orderbook:
            raise ValueError("No orderbook data available")
        
        best_ask = self.current_orderbook.asks[0].price
        best_bid = self.current_orderbook.bids[0].price
        return (best_ask + best_bid) / 2 