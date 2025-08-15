#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Require-Cmd($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) { throw "[error] $name not found" }
}

$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$RUN_DIR = Join-Path $ROOT ".run"
$BACKEND_PID_FILE = Join-Path $RUN_DIR "backend.pid"
$FRONTEND_PID_FILE = Join-Path $RUN_DIR "frontend.pid"
New-Item -ItemType Directory -Force -Path $RUN_DIR | Out-Null

function Stop-ByPidFile($file) {
  if (Test-Path $file) {
    $pid = Get-Content $file | Select-Object -First 1
    if ($pid -and (Get-Process -Id $pid -ErrorAction SilentlyContinue)) {
      try { Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue } catch {}
    }
    Remove-Item $file -ErrorAction SilentlyContinue
  }
}

# Idempotent: stop stale processes
Stop-ByPidFile $BACKEND_PID_FILE
Stop-ByPidFile $FRONTEND_PID_FILE

Write-Host "[1/8] Checking tools"
Require-Cmd docker
$hasCompose = $false
try { $null = docker compose version; $hasCompose = $true } catch {}
if (-not $hasCompose) { Require-Cmd docker-compose }
Require-Cmd python
Require-Cmd node

Write-Host "[2/8] Bringing up Postgres"
if ($hasCompose) { Push-Location $ROOT; docker compose up -d postgres; Pop-Location }
else { Push-Location $ROOT; docker-compose up -d postgres; Pop-Location }

Write-Host "[3/8] Waiting for Postgres"
$ok = $false
1..60 | ForEach-Object {
  try { if ((docker exec qanooni-postgres pg_isready -U qanooni -d qanooni) -like "*accepting connections*") { $ok = $true; break } } catch {}
  Start-Sleep -Seconds 1
}
if (-not $ok) { throw "[error] Postgres not ready" }

if (-not $env:DATABASE_URL) { $env:DATABASE_URL = "postgresql+psycopg2://qanooni:qanooni@localhost:5432/qanooni" }

Write-Host "[4/8] Backend venv + deps"
$venvDir = Join-Path $ROOT "backend\.venv"
if (-not (Test-Path $venvDir)) { python -m venv $venvDir }
& "$venvDir\Scripts\python.exe" -m pip install --disable-pip-version-check -r "$ROOT\backend\requirements.txt"

Write-Host "[5/8] Initialize DB schema (idempotent)"
$env:PYTHONPATH = "$ROOT\backend"
& "$venvDir\Scripts\python.exe" -c "import os; from app.db import init_db; print('[init] DATABASE_URL =', os.getenv('DATABASE_URL')); init_db(); print('[ok] DB initialized')"

Write-Host "[6/8] Frontend deps"
Push-Location "$ROOT\frontend"
if (Get-Command yarn -ErrorAction SilentlyContinue) { yarn install }
else { npm install --no-audit --no-fund --silent }
Write-Host "[6.1/8] Playwright browsers"
if (Get-Command yarn -ErrorAction SilentlyContinue) { yarn playwright install }
else { npx playwright install }
Write-Host "[6.2/8] MSW service worker"
if (Get-Command yarn -ErrorAction SilentlyContinue) { yarn msw:init }
else { npx msw init public --save }
Pop-Location

Write-Host "[7/8] Start backend and frontend"
$BACKEND_LOG = "$ROOT\backend\backend.log"
$FRONTEND_LOG = "$ROOT\frontend\frontend.log"
Remove-Item $BACKEND_LOG, $FRONTEND_LOG -ErrorAction SilentlyContinue

# Start backend
$backend = Start-Process -FilePath "$venvDir\Scripts\python.exe" -ArgumentList "-m","uvicorn","app.main:app","--app-dir","$ROOT\backend","--port","8000" -NoNewWindow -RedirectStandardOutput $BACKEND_LOG -RedirectStandardError $BACKEND_LOG -PassThru
$backend.Id | Out-File -FilePath $BACKEND_PID_FILE -Encoding ascii -Force

# Start frontend
if (Get-Command yarn -ErrorAction SilentlyContinue) {
  $frontend = Start-Process -FilePath "yarn" -ArgumentList "dev" -WorkingDirectory "$ROOT\frontend" -NoNewWindow -RedirectStandardOutput $FRONTEND_LOG -RedirectStandardError $FRONTEND_LOG -PassThru
} else {
  $frontend = Start-Process -FilePath "npm" -ArgumentList "run","dev","--silent" -WorkingDirectory "$ROOT\frontend" -NoNewWindow -RedirectStandardOutput $FRONTEND_LOG -RedirectStandardError $FRONTEND_LOG -PassThru
}
$frontend.Id | Out-File -FilePath $FRONTEND_PID_FILE -Encoding ascii -Force

Write-Host "[8/8] Warmup check"
$ok = $false
1..30 | ForEach-Object {
  try { Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/api/dashboard | Out-Null; $ok = $true; break } catch { Start-Sleep -Seconds 1 }
}
if ($ok) { Write-Host "[ok] Backend responding" } else { Write-Host "[warn] Backend not responding yet; see $BACKEND_LOG" }

Write-Host "[info] Frontend: http://127.0.0.1:5173"
Write-Host "[info] Backend:  http://127.0.0.1:8000"
Write-Host "[logs] Backend:  $BACKEND_LOG"
Write-Host "[logs] Frontend: $FRONTEND_LOG"
Write-Host "`nPress Ctrl+C to stop."

try {
  Wait-Process -Id $backend.Id,$frontend.Id
} finally {
  Stop-ByPidFile $BACKEND_PID_FILE
  Stop-ByPidFile $FRONTEND_PID_FILE
}