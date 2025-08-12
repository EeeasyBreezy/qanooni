#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[setup] Backend venv"
if [[ ! -d "$ROOT_DIR/backend/.venv" ]]; then
  python3 -m venv "$ROOT_DIR/backend/.venv"
fi
source "$ROOT_DIR/backend/.venv/bin/activate"
pip install --disable-pip-version-check --quiet -r "$ROOT_DIR/backend/requirements.txt"

echo "[setup] Frontend deps"
pushd "$ROOT_DIR/frontend" >/dev/null
npm install --no-audit --no-fund --silent
popd >/dev/null

echo "[dev] Starting backend on :8000 and frontend on :5173"

# Start backend
(
  cd "$ROOT_DIR/backend"
  exec uvicorn app.main:app --app-dir "$ROOT_DIR/backend" --reload --port 8000
) &
BACKEND_PID=$!

# Start frontend
(
  cd "$ROOT_DIR/frontend"
  exec npm run dev --silent
) &
FRONTEND_PID=$!

cleanup() {
  echo "\n[dev] Shutting down..."
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
  wait $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
}
trap cleanup INT TERM EXIT

wait


