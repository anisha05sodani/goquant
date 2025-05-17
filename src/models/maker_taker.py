import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from sklearn.linear_model import LogisticRegression

@dataclass
class OrderBookSnapshot:
    timestamp: float
    spread: float
    depth: float
    volume: float
    volatility: float

class MakerTakerPredictor:
    def __init__(self):
        self.model = LogisticRegression()
        self.orderbook_history: List[OrderBookSnapshot] = []
        self.maker_taker_history: List[float] = []  # Proportion of maker orders
        
    def update(self, 
               spread: float, 
               depth: float, 
               volume: float, 
               volatility: float,
               maker_proportion: float) -> None:
        """Update the model with new orderbook data"""
        snapshot = OrderBookSnapshot(
            timestamp=len(self.orderbook_history),
            spread=spread,
            depth=depth,
            volume=volume,
            volatility=volatility
        )
        
        self.orderbook_history.append(snapshot)
        self.maker_taker_history.append(maker_proportion)
        
    def predict_maker_proportion(self, 
                               spread: float, 
                               depth: float, 
                               volume: float, 
                               volatility: float) -> float:
        """Predict the proportion of maker orders"""
        if len(self.orderbook_history) < 10:  # Need minimum data for training
            return 0.5  # Default to 50/50 split
            
        # Prepare features for training
        X = np.array([[s.spread, s.depth, s.volume, s.volatility] 
                      for s in self.orderbook_history])
        y = np.array(self.maker_taker_history)
        
        # Train model
        self.model.fit(X, y)
        
        # Predict for new data
        features = np.array([[spread, depth, volume, volatility]])
        prediction = self.model.predict_proba(features)[0][1]  # Probability of maker order
        
        return float(prediction) 