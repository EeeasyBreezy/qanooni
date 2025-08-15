Backend (FastAPI)

Dev

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Postgres + pgvector

```
docker compose up -d postgres
export DATABASE_URL=postgresql+psycopg2://qanooni:qanooni@localhost:5432/qanooni
```

Endpoints:
- GET /api/health
- GET /api/greeting?name=YourName

OCR

Prerequisites:
- Install Tesseract OCR
  - macOS (Homebrew):
    - `brew install tesseract`
    - optional: `brew install tesseract-lang`

Endpoint:
- POST `/ocr/extract` with `multipart/form-data` field `image` (JPEG/PNG)
- Response JSON:
  - `language`: detected language code
  - `text`: recognized text
  - `tables`: list of simple table matrices (heuristic)


