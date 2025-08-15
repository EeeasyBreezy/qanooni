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

### One command dev
From the project root:
```bash
./run.sh
```
This installs deps if needed and runs both servers concurrently:
- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5173`


### Prerequisites
- Docker and Docker Compose
- Python 3 (on PATH as `python3` or `python`)
- Node.js (and optionally Yarn)

### One-command dev (shell choice)
- Bash/Zsh/Fish (macOS/Linux): run `./dev_up.sh`
- PowerShell (Windows/macOS): run `./dev_up.ps1`

Both scripts:
- Auto-create a virtualenv under `backend/.venv`
- Install backend and frontend dependencies
- Bring up Postgres with Docker
- Start backend and frontend and write logs to `backend/backend.log` and `frontend/frontend.log`
