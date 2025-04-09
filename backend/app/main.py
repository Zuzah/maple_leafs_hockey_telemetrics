from fastapi import FastAPI
from .api import metrics, simulator


app = FastAPI(title="Maple Leafs Hockey Telemetrics API")

# Routers
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
app.include_router(simulator.router, prefix="/simulate", tags=["Simulator"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Maple Leafs Hockey Telemetrics API"}
