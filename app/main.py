from fastapi import FastAPI, BackgroundTasks
import httpx
import asyncio
from .models import VehicleValuationRequest, VideoViewRequest

app = FastAPI(
    title="Vehicle Valuation & Traffic Simulation API",
    description="University Assignment API integrating asynchronous endpoints."
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Backend"}

@app.post("/api/v1/valuate")
def valuate_vehicle(request: VehicleValuationRequest):
    # Mock valuation logic based on year and model
    base_price = 15000
    if request.year > 2020:
        base_price += 5000
    return {"vehicle": request.model, "estimated_value": base_price, "currency": "USD"}

async def bot_views_task(url: str, count: int):
    # Educational purpose only: simulate asynchronous requests to a URL
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for _ in range(count)]
        # Execute concurrently
        await asyncio.gather(*tasks, return_exceptions=True)

@app.post("/api/v1/simulate-views")
async def simulate_views(request: VideoViewRequest, background_tasks: BackgroundTasks):
    """
    Educational endpoint to simulate traffic/views to a given video link asynchronously.
    """
    background_tasks.add_task(bot_views_task, request.url, request.view_count)
    return {"message": f"Started simulating {request.view_count} views for {request.url} in the background."}
