from dataclasses import dataclass
from typing import Dict

@dataclass
class TradingConfig:
    # WebSocket settings
    ws_url: str = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
    ws_reconnect_interval: int = 5  # seconds
    
    # Trading parameters
    default_quantity: float = 100.0  # USD
    default_volatility: float = 0.02
    fee_tiers: Dict[str, float] = {
        "Tier 1": 0.001,  # 0.1%
        "Tier 2": 0.0008,  # 0.08%
        "Tier 3": 0.0006,  # 0.06%
    }
    
    # Model parameters
    market_impact_eta: float = 0.1
    market_impact_gamma: float = 0.1
    time_horizon: float = 1.0  # hours
    
    # Performance settings
    max_processing_time: float = 100.0  # ms
    performance_window: int = 100  # number of samples to keep
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'TradingConfig':
        """Load configuration from JSON file"""
        if not os.path.exists(filepath):
            return cls()
            
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls(**data)
    
    def save_to_file(self, filepath: str):
        """Save configuration to JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.__dict__, f, indent=4) 