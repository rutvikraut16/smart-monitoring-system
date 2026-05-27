from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio, json, random, time, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/", response_class=HTMLResponse)
def home():
    path = os.path.join(BASE_DIR, "templates", "index.html")
    with open(path, encoding="utf-8") as f:
        return f.read()

@app.get("/api/sensor")
def get_sensor():
    temp = random.randint(20, 100)
    return {
        "temperature": temp,
        "humidity":    random.randint(30, 90),
        "pressure":    random.randint(995, 1025),
        "cpu":         random.randint(10, 95),
        "timestamp":   time.strftime("%H:%M:%S"),
        "status":      "HIGH" if temp > 70 else "NORMAL"
    }

async def sensor_event_generator():
    while True:
        temp = random.randint(20, 100)
        data = {
            "temperature": temp,
            "humidity":    random.randint(30, 90),
            "pressure":    random.randint(995, 1025),
            "cpu":         random.randint(10, 95),
            "timestamp":   time.strftime("%H:%M:%S"),
            "status":      "HIGH" if temp > 70 else "NORMAL"
        }
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(2)

@app.get("/api/stream")
async def stream():
    return StreamingResponse(
        sensor_event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )