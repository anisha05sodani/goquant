import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from sklearn.linear_model import QuantileRegressor

@dataclass
class OrderBookLevel:
    price: float
    quantity: float

class SlippageEstimator:
    def __init__(self, quantile: float = 0.5):
        self.quantile = quantile
        self.model = QuantileRegressor(quantile=quantile)
        self.price_history: List[float] = []
        self.volume_history: List[float] = []
        self.slippage_history: List[float] = []
        
    def update(self, orderbook_levels: List[OrderBookLevel], executed_quantity: float) -> float:
        """
        Update the model with new orderbook data and calculate slippage.
        Returns the estimated slippage in basis points.
        """
        if not orderbook_levels:
            return 0.0
            
        # Calculate volume-weighted average price (VWAP)
        total_volume = sum(level.quantity for level in orderbook_levels)
        vwap = sum(level.price * level.quantity for level in orderbook_levels) / total_volume
        
        # Calculate mid price
        mid_price = (orderbook_levels[0].price + orderbook_levels[-1].price) / 2
        
        # Calculate slippage
        slippage = (vwap - mid_price) / mid_price * 10000  # in basis points
        
        # Update history
        self.price_history.append(mid_price)
        self.volume_history.append(total_volume)
        self.slippage_history.append(slippage)
        
        return slippage
    
    def predict_slippage(self, quantity: float) -> float:
        """
        Predict slippage for a given quantity using the trained model.
        Returns the predicted slippage in basis points.
        """
        if len(self.price_history) < 2:
            return 0.0
            
        # Prepare features for prediction
        X = np.array(self.volume_history).reshape(-1, 1)
        y = np.array(self.slippage_history)
        
        # Train model
        self.model.fit(X, y)
        
        # Predict slippage for the given quantity
        predicted_slippage = self.model.predict([[quantity]])[0]
        
        return max(0.0, predicted_slippage)  # Slippage should be non-negative 