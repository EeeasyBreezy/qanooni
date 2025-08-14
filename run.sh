#!/usr/bin/env bash
set -euo pipefail

# Enable debug mode with DEBUG=1 ./run.sh
if [[ "${DEBUG:-0}" == "1" ]]; then
  set -x
fi

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Basic env checks
command -v python3 >/dev/null 2>&1 || { echo "[error] python3 not found"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "[error] node not found"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "[error] npm not found"; exit 1; }

echo "[setup] Backend venv"
if [[ ! -d "$ROOT_DIR/backend/.venv" ]]; then
  python3 -m venv "$ROOT_DIR/backend/.venv"
fi
source "$ROOT_DIR/backend/.venv/bin/activate"

# Less quiet when debugging
PIP_FLAGS=(--disable-pip-version-check --quiet)
if [[ "${DEBUG:-0}" == "1" ]]; then PIP_FLAGS=(); fi

echo "[setup] Installing backend requirements"
pip install "${PIP_FLAGS[@]}" -r "$ROOT_DIR/backend/requirements.txt"

echo "[setup] Frontend deps"
pushd "$ROOT_DIR/frontend" >/dev/null
NPM_FLAGS=(--no-audit --no-fund --silent)
if [[ "${DEBUG:-0}" == "1" ]]; then NPM_FLAGS=(--no-audit --no-fund); fi
npm install "${NPM_FLAGS[@]}"
popd >/dev/null

export PYTHONUNBUFFERED=1
echo "[dev] Starting backend on :8000 and frontend on :5173"

# Log files
BACKEND_LOG="$ROOT_DIR/backend/backend.log"
FRONTEND_LOG="$ROOT_DIR/frontend/frontend.log"
rm -f "$BACKEND_LOG" "$FRONTEND_LOG" || true

# Start backend
(
  cd "$ROOT_DIR/backend"
  exec uvicorn app.main:app --app-dir "$ROOT_DIR/backend" --reload --port 8000 >"$BACKEND_LOG" 2>&1
) &
BACKEND_PID=$!

# Start frontend
(
  cd "$ROOT_DIR/frontend"
  if [[ "${DEBUG:-0}" == "1" ]]; then
    exec npm run dev >"$FRONTEND_LOG" 2>&1
  else
    exec npm run dev --silent >"$FRONTEND_LOG" 2>&1
  fi
) &
FRONTEND_PID=$!

cleanup() {
  echo "\n[dev] Shutting down..."
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
  wait $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
}
trap cleanup INT TERM EXIT

echo "[dev] Logs:"
echo "  Backend: $BACKEND_LOG"
echo "  Frontend: $FRONTEND_LOG"

wait || {
  echo "[dev] One of the processes exited. Tail logs above for details.";
  exit 1;
}


