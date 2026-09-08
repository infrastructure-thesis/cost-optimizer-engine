"""Cost recommendation engine."""
from dataclasses import dataclass

@dataclass
class Recommendation:
    resource_id: str
    current_cost_monthly: float
    recommended_cost_monthly: float
    annual_savings: float
    description: str
    
class CostRecommender:
    """Generate cost optimization recommendations."""
    
    def analyze(self, resource_id: str, utilization: float) -> Recommendation | None:
        """Analyze resource and return recommendation if optimization found."""
        # If utilization < 10%, recommend right-sizing
        if utilization < 10:
            return Recommendation(
                resource_id=resource_id,
                current_cost_monthly=100.0,
                recommended_cost_monthly=25.0,
                annual_savings=900.0,
                description=f"Right-size {resource_id}: currently at {utilization}% utilization"
            )
        return None
