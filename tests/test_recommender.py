"""Test cost recommender."""
import pytest
from src.cost_recommender.recommender import CostRecommender

def test_recommender_low_utilization():
    """Test recommendation for low utilization."""
    recommender = CostRecommender()
    rec = recommender.analyze("instance-1", utilization=5.0)
    
    assert rec is not None
    assert rec.resource_id == "instance-1"
    assert rec.annual_savings == 900.0
    
def test_recommender_high_utilization():
    """Test no recommendation for high utilization."""
    recommender = CostRecommender()
    rec = recommender.analyze("instance-1", utilization=80.0)
    
    assert rec is None

def test_recommender_boundary():
    """Test boundary at 10% utilization."""
    recommender = CostRecommender()
    rec = recommender.analyze("instance-1", utilization=10.0)
    
    # At exactly 10%, should not recommend
    assert rec is None

def test_recommender_just_below_boundary():
    """Test just below 10% boundary."""
    recommender = CostRecommender()
    rec = recommender.analyze("instance-1", utilization=9.9)
    
    assert rec is not None  # Should recommend because 9.9 < 10

def test_recommendation_structure():
    """Test recommendation has correct fields."""
    recommender = CostRecommender()
    rec = recommender.analyze("instance-1", utilization=5.0)
    
    assert hasattr(rec, 'resource_id')
    assert hasattr(rec, 'current_cost_monthly')
    assert hasattr(rec, 'recommended_cost_monthly')
    assert hasattr(rec, 'annual_savings')
    assert hasattr(rec, 'description')

def test_cost_savings_calculation():
    """Test cost savings are calculated correctly."""
    recommender = CostRecommender()
    rec = recommender.analyze("instance-1", utilization=5.0)
    
    # Annual savings = (100 - 25) * 12 = 900
    assert rec.annual_savings == 900.0
    assert rec.annual_savings == (rec.current_cost_monthly - rec.recommended_cost_monthly) * 12

def test_multiple_resources():
    """Test analysis of mulitple resources."""
    recommender = CostRecommender()
    rec1 = recommender.analyze("instance-1", utilization=5.0)
    rec2 = recommender.analyze("instance-2", utilization=50.0)
    rec3 = recommender.analyze("instance-3", utilization=8.0)
    
    assert rec1 is not None
    assert rec2 is None
    assert rec3 is not None

def test_description_includes_utilization():
    """Test description includes utilization info."""
    recommender = CostRecommender()
    rec = recommender.analyze("db-prod-01", utilization=7.5)

    assert "7.5" in rec.description
    assert "db-prod-01" in rec.description
