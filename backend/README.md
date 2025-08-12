Backend (FastAPI)

Dev

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Endpoints:
- GET /api/health
- GET /api/greeting?name=YourName


