## FastAPI + React (TypeScript) Starter

### Backend (FastAPI)
1) Create venv and install deps
```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
```
2) Run API
```bash
uvicorn app.main:app --app-dir backend --reload --port 8000
```

### Frontend (React + Vite + TS)
```bash
cd frontend
npm install
npm run dev
```

The frontend dev server proxies `/api/*` to `http://127.0.0.1:8000`.


