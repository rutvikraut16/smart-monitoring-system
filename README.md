# Smart Monitoring System 🚨

A Real-Time IoT Dashboard that simulates sensor data, streams it live to a web browser, and triggers visual alerts when values cross danger thresholds.

## Tech Stack
- Python 3.11
- FastAPI + Uvicorn
- Apache Kafka + Zookeeper
- Docker + Docker Compose
- Streamlit
- Chart.js
- Server-Sent Events (SSE)

## Sensors Monitored
| Sensor | Range | Danger Threshold |
|---|---|---|
| Temperature | 20–100°C | > 70°C |
| Humidity | 30–90% | > 80% |
| Pressure | 995–1025 hPa | > 1020 hPa |
| CPU Load | 10–95% | > 80% |

## How to Run

### With Docker
```bash
docker-compose up --build
```

### Without Docker
```bash
pip install -r requirements.txt
uvicorn app:app --reload
streamlit run streamlit_app.py
```

## Project Structure
| File | Role |
|---|---|
| app.py | FastAPI server + SSE stream |
| sensor_simulator.py | Generates random sensor data |
| producer.py | Kafka producer |
| consumer.py | Kafka consumer |
| ai_service.py | AI alert detection |
| streamlit_app.py | Live Streamlit dashboard |
| Dockerfile | Docker image config |
| docker-compose.yml | Multi-service startup |
| templates/index.html | Browser dashboard |
