# cost-optimizer-engine

Identifies $200k-$800k in annual infrastructure optimization without reducing SLA.

## Quick Start

### Install
```bash
make install
```

### Run Tests
```bash
make test
```

### Start API
```bash
make run
```

Then visit: `http://localhost:8000/docs`

## Test Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get recommendation (low utilization)
curl "http://localhost:8000/recommend?resource_id=instance-1&utilization=5"

# Get recommendation (high utilization - no recommendation)
curl "http://localhost:8000/recommend?resource_id=instance-1&utilization=80"
```

## Features

- **ML Capacity Recommender:** Identifies underutilized resources
- **Cost Projection:** Before/after cost comparison
- **Multi-Cloud Parity:** AWS/GCP/Azure cost comparison (coming Week 2)
- **Dashboard:** Real-time cost visibility (coming Week 3)

## Architecture

CloudWatch Metrics ↓ ML Recommender (scikit-learn) ↓ FastAPI Endpoint ↓ Cost Analysis ↓ Recommendations

## Status

- ✅ API running
- ✅ Tests passing
- ✅ Documentation
- 🔄 Terraform integration (Week 2)
- 🔄 Multi-cloud parity (Week 3)
- 🔄 Dashboard (Week 4)

## License

Apache 2.0
