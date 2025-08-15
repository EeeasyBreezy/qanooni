Integration tests (HTTP-level)

How to run locally:
- Ensure Postgres is running (docker compose up -d postgres)
- Start the dev server (./dev_up.sh or dev_up.ps1), or run backend separately on :8000
- In another terminal: python -m pytest -q tests_integration


