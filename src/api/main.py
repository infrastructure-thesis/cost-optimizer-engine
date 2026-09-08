"""FastAPI application."""
from fastapi import FastAPI
from src.cost_recommender.recommender import CostRecommender, Recommendation

app = FastAPI(
    title="cost-optimizer-engine",
    description="ML-driven cost optimization for fintech",
    version="0.1.0",
)

recommender = CostRecommender()

@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}

@app.post("/recommend")
async def get_recommendations(resource_id: str, utilization: float) -> dict:
    """Get cost recommendations."""
    rec = recommender.analyze(resource_id, utilization)
    
    if rec:
        return {
            "resource_id": rec.resource_id,
            "current_cost_monthly": rec.current_cost_monthly,
            "recommended_cost_monthly": rec.recommended_cost_monthly,
            "annual_savings": rec.annual_savings,
            "description": rec.description,
        }
        
    return {"message": "No recommendations"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    