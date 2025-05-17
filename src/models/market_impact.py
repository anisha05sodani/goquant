import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class MarketImpactParams:
    eta: float  # Temporary market impact parameter
    gamma: float  # Permanent market impact parameter
    sigma: float  # Volatility
    tau: float  # Time horizon
    initial_price: float  # Initial price
    total_quantity: float  # Total quantity to execute

class AlmgrenChrissModel:
    def __init__(self, params: MarketImpactParams):
        self.params = params
        
    def calculate_optimal_execution(self) -> Tuple[List[float], List[float]]:
        """
        Calculate optimal execution trajectory using Almgren-Chriss model.
        Returns tuple of (times, quantities) for the optimal execution path.
        """
        # Model parameters
        eta = self.params.eta
        gamma = self.params.gamma
        sigma = self.params.sigma
        tau = self.params.tau
        X = self.params.total_quantity
        P0 = self.params.initial_price
        
        # Calculate optimal trading rate
        kappa = np.sqrt(gamma / eta)
        
        # Generate time points
        t = np.linspace(0, tau, 100)
        
        # Calculate optimal execution trajectory
        x = X * (np.sinh(kappa * (tau - t)) / np.sinh(kappa * tau))
        
        return t, x
    
    def calculate_market_impact(self, quantity: float, time: float) -> float:
        """
        Calculate market impact for a given quantity and time.
        Returns the price impact in basis points.
        """
        eta = self.params.eta
        gamma = self.params.gamma
        sigma = self.params.sigma
        
        # Temporary impact
        temp_impact = eta * (quantity / time) * (sigma / np.sqrt(time))
        
        # Permanent impact
        perm_impact = gamma * quantity
        
        # Total impact in basis points
        total_impact = (temp_impact + perm_impact) / self.params.initial_price * 10000
        
        return total_impact
    
    def estimate_execution_cost(self, quantity: float, time: float) -> float:
        """
        Estimate total execution cost including market impact.
        Returns the total cost in the quote currency.
        """
        impact = self.calculate_market_impact(quantity, time)
        cost = quantity * self.params.initial_price * (1 + impact/10000)
        return cost 