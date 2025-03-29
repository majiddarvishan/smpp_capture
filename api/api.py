from fastapi import FastAPI
from api.routes import smpp_routes, healthcheck

app = FastAPI(
    title="SMPP Insights API",
    description="API for querying SMPP transactions, latency metrics, alerts, and health checks",
    version="1.0.0"
)

# Include routes
app.include_router(smpp_routes.router, prefix="/api", tags=["SMPP Insights"])
app.include_router(healthcheck.router, prefix="/api", tags=["Health Checks"])

@app.get("/")
def root():
    """
    Root endpoint to indicate API is running.
    """
    return {"message": "SMPP Insights API is running. Use /docs for API documentation."}
