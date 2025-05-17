import pytest
from src.models.market_impact import AlmgrenChrissModel, MarketImpactParams

@pytest.fixture
def market_impact_params():
    return MarketImpactParams(
        eta=0.1,
        gamma=0.1,
        sigma=0.02,
        tau=1.0,
        initial_price=50000.0,
        total_quantity=1.0
    )

@pytest.fixture
def market_impact_model(market_impact_params):
    return AlmgrenChrissModel(market_impact_params)

def test_optimal_execution(market_impact_model):
    times, quantities = market_impact_model.calculate_optimal_execution()
    
    assert len(times) == 100
    assert len(quantities) == 100
    assert quantities[0] == market_impact_model.params.total_quantity
    assert quantities[-1] == 0.0

def test_market_impact_calculation(market_impact_model):
    impact = market_impact_model.calculate_market_impact(1.0, 1.0)
    assert impact >= 0
    assert isinstance(impact, float) 