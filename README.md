## FastAPI + React (TypeScript) – Development

### Prerequisites
- Docker Desktop with Docker Compose
- Python 3 (available as `python3` or `python` on PATH)
- Node.js 18+ (required by Playwright). Optional: Yarn

### Start everything with one command
- Bash/Zsh (macOS/Linux):
```bash
./dev_up.sh
```
- PowerShell (Windows/macOS):
```powershell
./dev_up.ps1
```

What these scripts do:
- Create `backend/.venv` and install backend deps
- Bring up Postgres via Docker (`qanooni-postgres`)
- Initialize the DB schema (pgvector + tables)
- Install frontend deps (+ Playwright browsers, MSW worker)
- Start backend on `http://127.0.0.1:8000` and frontend on `http://127.0.0.1:5173`
- Logs: `backend/backend.log`, `frontend/frontend.log`

Optional: run backend integration tests during startup by setting an env variable before launching:
```bash
DEV_RUN_IT=1 ./dev_up.sh
```
```powershell
$env:DEV_RUN_IT = "1"; ./dev_up.ps1
```

### Backend tests
- Unit tests:
```bash
cd backend
source .venv/bin/activate
pytest -q
```

- Integration tests (HTTP-level): ensure Postgres and backend are running (the dev scripts do this), then:
```bash
cd backend
source .venv/bin/activate
python -m pytest -q tests_integration
```
You can also opt-in to run them automatically at startup with `DEV_RUN_IT=1` as shown above.

### Frontend end-to-end tests (Playwright)
Requirements: Node 18+, browsers installed once via Playwright.
```bash
cd frontend
yarn install || npm install
yarn playwright install || npx playwright install

# Run with mocked API via MSW
yarn e2e || npm run e2e
```
Notes:
- E2E tests use MSW mocks and start the dev server automatically (`start-server-and-test`).
- Base URL and MSW storage state are configured in `frontend/playwright.config.ts`.
