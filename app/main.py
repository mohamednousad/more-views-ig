import asyncio
import httpx
from fastapi import FastAPI, BackgroundTasks, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from duckduckgo_search import DDGS
from pydantic import BaseModel

app = FastAPI(title="Unified API with AI & Bot Simulation")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Mock Database for Task Tracking
task_store = {}

# Pydantic Models
class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 1. Bot Simulation API (Educational Purpose)
async def simulate_bot_traffic(task_id: str, target_url: str, requests_count: int):
    task_store[task_id] = {"status": "Running", "completed": 0, "target": target_url}
    logger.info(f"Task {task_id} started for {requests_count} hits on {target_url}")
    
    async with httpx.AsyncClient(verify=False) as client:
        for _ in range(requests_count):
            try:
                headers = {"User-Agent": "Mozilla/5.0 Bot-Educational-Simulation"}
                await client.get(target_url, headers=headers, timeout=5.0)
                task_store[task_id]["completed"] += 1
            except Exception:
                pass
            await asyncio.sleep(0.5)
            
    task_store[task_id]["status"] = "Completed"

@app.post("/api/bot/simulate")
async def start_bot_simulation(
    background_tasks: BackgroundTasks, 
    video_url: str = Form(...), 
    view_count: int = Form(...)
):
    task_id = "TASK-" + str(len(task_store) + 1)
    background_tasks.add_task(simulate_bot_traffic, task_id, video_url, view_count)
    return {"status": "Success", "task_id": task_id, "message": f"Bot simulation started."}

@app.get("/api/bot/status/{task_id}")
async def get_status(task_id: str):
    return task_store.get(task_id, {"status": "Not Found"})

# 2. Free External API (Public Data)
@app.get("/api/external/quote")
async def get_random_quote():
    async with httpx.AsyncClient() as client:
        try:
            # Using DummyJSON for free public external API data
            resp = await client.get("https://dummyjson.com/quotes/random")
            data = resp.json()
            return {"quote": data.get("quote"), "author": data.get("author")}
        except Exception as e:
            return {"error": "Failed to fetch external API"}

# 3. Free AI API (DuckDuckGo No-Key AI)
@app.post("/api/ai/chat")
async def chat_with_free_ai(req: ChatRequest):
    try:
        results = DDGS().chat(req.message, model="gpt-4o-mini")
        return {"response": results}
    except Exception as e:
        logger.error(f"AI Error: {e}")
        return {"response": "The AI is currently resting. Try again!"}
