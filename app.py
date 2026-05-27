from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import random

app = FastAPI()

# Static CSS folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="templates")

# Dummy sensor data
sensor_data = {
    "temperature": 40,
    "status": "NORMAL"
}

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):

    # Random demo updates
    temp = random.randint(20, 100)

    status = "NORMAL"

    if temp > 70:
        status = "HIGH ALERT"

    sensor_data["temperature"] = temp
    sensor_data["status"] = status

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "temperature": sensor_data["temperature"],
            "status": sensor_data["status"]
        }
    )