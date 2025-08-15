#!/usr/bin/env bash
set -euo pipefail
if [[ "${DEBUG:-0}" == "1" ]]; then set -x; fi

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_PID_FILE="$ROOT_DIR/.run/backend.pid"
FRONTEND_PID_FILE="$ROOT_DIR/.run/frontend.pid"

mkdir -p "$ROOT_DIR/.run"

# Kill prior app processes from previous runs (idempotent)
kill_if_running() {
  local pid_file="$1"
  if [[ -f "$pid_file" ]]; then
    local pid
    pid="$(cat "$pid_file" || true)"
    if [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
      # wait briefly
      for _ in {1..10}; do kill -0 "$pid" 2>/dev/null || break; sleep 0.2; done
    fi
    rm -f "$pid_file"
  fi
}
kill_if_running "$BACKEND_PID_FILE"
kill_if_running "$FRONTEND_PID_FILE"

echo "[1/8] Checking tools"
command -v docker >/dev/null 2>&1 || { echo "[error] docker not found"; exit 1; }
if command -v docker compose >/dev/null 2>&1; then COMPOSE="docker compose"; else
  command -v docker-compose >/dev/null 2>&1 || { echo "[error] docker compose not found"; exit 1; }
  COMPOSE="docker-compose"
fi
command -v python3 >/dev/null 2>&1 || { echo "[error] python3 not found"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "[error] node not found"; exit 1; }

echo "[2/8] Bringing up Postgres"
(cd "$ROOT_DIR" && $COMPOSE up -d postgres)

echo "[3/8] Waiting for Postgres"
for i in {1..60}; do
  if docker exec qanooni-postgres pg_isready -U qanooni -d qanooni >/dev/null 2>&1; then
    echo "[ok] Postgres is ready"; break
  fi
  sleep 1
  [[ $i -eq 60 ]] && { echo "[error] Postgres not ready"; exit 1; }
done

export DATABASE_URL="${DATABASE_URL:-postgresql+psycopg2://qanooni:qanooni@localhost:5432/qanooni}"

echo "[4/8] Backend venv + deps"
if [[ ! -d "$ROOT_DIR/backend/.venv" ]]; then python3 -m venv "$ROOT_DIR/backend/.venv"; fi
# shellcheck source=/dev/null
source "$ROOT_DIR/backend/.venv/bin/activate"
pip install --disable-pip-version-check -r "$ROOT_DIR/backend/requirements.txt"

echo "[5/8] Initialize DB schema (idempotent)"
PYTHONPATH="$ROOT_DIR/backend" python - <<'PY'
import os
from app.db import init_db
print("[init] DATABASE_URL =", os.getenv("DATABASE_URL"))
init_db()
print("[ok] DB initialized")
PY

echo "[6/8] Frontend deps"
pushd "$ROOT_DIR/frontend" >/dev/null
if command -v yarn >/dev/null 2>&1; then yarn -s install; else npm install --no-audit --no-fund --silent; fi
echo "[6.1/8] Playwright browsers"
if command -v yarn >/dev/null 2>&1; then yarn -s playwright install; else npx playwright install >/dev/null 2>&1 || ./node_modules/.bin/playwright install; fi
popd >/dev/null

echo "[7/8] Start backend and frontend"
BACKEND_LOG="$ROOT_DIR/backend/backend.log"
FRONTEND_LOG="$ROOT_DIR/frontend/frontend.log"
rm -f "$BACKEND_LOG" "$FRONTEND_LOG" || true

( cd "$ROOT_DIR/backend" && exec uvicorn app.main:app --app-dir "$ROOT_DIR/backend" --port 8000 >"$BACKEND_LOG" 2>&1 ) &
BACKEND_PID=$!
echo "$BACKEND_PID" > "$BACKEND_PID_FILE"

( cd "$ROOT_DIR/frontend" && if command -v yarn >/dev/null 2>&1; then exec yarn -s dev >"$FRONTEND_LOG" 2>&1; else exec npm run dev --silent >"$FRONTEND_LOG" 2>&1; fi ) &
FRONTEND_PID=$!
echo "$FRONTEND_PID" > "$FRONTEND_PID_FILE"

echo "[8/8] Warmup check"
warm_ok=0
if command -v curl >/dev/null 2>&1; then
  for i in {1..30}; do curl -fsS http://127.0.0.1:8000/api/dashboard >/dev/null && { warm_ok=1; break; } || true; sleep 1; done
elif command -v wget >/dev/null 2>&1; then
  for i in {1..30}; do wget -qO- http://127.0.0.1:8000/api/dashboard >/dev/null && { warm_ok=1; break; } || true; sleep 1; done
else
  echo "[warn] curl/wget not found; skipping warmup"
fi
[[ $warm_ok -eq 1 ]] && echo "[ok] Backend responding" || echo "[warn] Backend not responding yet (see $BACKEND_LOG)"

echo "[info] Frontend: http://127.0.0.1:5173"
echo "[info] Backend:  http://127.0.0.1:8000"
echo "[logs] Backend:  $BACKEND_LOG"
echo "[logs] Frontend: $FRONTEND_LOG"

cleanup() {
  echo; echo "[dev] Shutting down…"
  kill_if_running "$BACKEND_PID_FILE"
  kill_if_running "$FRONTEND_PID_FILE"
}
trap cleanup INT TERM EXIT
wait