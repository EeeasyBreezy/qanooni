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

## How the system works

### High-level architecture
- Backend: FastAPI app with Postgres (+ pgvector) for vector search
- Frontend: React + TypeScript with MSW for mocks and Playwright for E2E
- Embeddings: Local Sentence-Transformers model (`all-MiniLM-L6-v2`) for both documents and queries
- Processing model: async upload → background processing → SSE notifications → query and dashboard APIs

### Data flow
1) Upload
   - Endpoint: `POST /upload` (multipart file + `request_id`)
   - Validates file type and content; maps to internal `File` model
   - Enqueues the file to a background worker (`UploadService`)
   - Immediately returns `202 Accepted`
   - Clients can subscribe to `GET /notifications/stream/{request_id}` (SSE) for completion

2) Background processing (`UploadService`)
   - Extract text using `TextExtractor` (with OCR for images inside PDFs as needed)
   - Derive metadata via `MetadataExtractor`
   - Chunk text using `TextChunker` (configurable window/overlap)
   - Generate embeddings with `LocalEmbeddingService`
   - Persist `Document` and `DocumentChunk` rows (including embeddings) via repository into Postgres/pgvector

3) Querying
   - Endpoint: `GET /query` with `question`, `limit`, `offset`
   - Embeds the question; optionally infers filters (agreement type, jurisdiction) from the question via `MetadataExtractor`
   - Performs vector search over chunks; picks best-scoring chunk per document
   - Returns a paged list of documents with top scores and basic metadata

4) Dashboard
   - Endpoints under `/dashboard` aggregate counts by agreement type, country, and industry for UI charts/tables

Key backend services and where they are wired:
- DI/providers in `backend/app/dependencies.py`
- Upload flow in `backend/app/routes/controllers/upload.py` → `UploadService`
- Query flow in `backend/app/routes/controllers/query.py` → `DocumentQueryService`
- SSE notifications in `backend/app/routes/controllers/notifications.py`

## Future LLM integration points

You can plug an LLM in multiple places to improve relevance and UX:

- Answer generation (RAG)
  - Extend `DocumentQueryService.run_query` to: retrieve top-K chunks → compose a prompt → call an LLM → return an answer + sources.
  - Keep existing vector search for grounding; add an `IAnsweringService` interface to swap providers (OpenAI, Anthropic, local models).

- Query understanding
  - Use an LLM to rewrite/expand the user question, extract structured filters (jurisdiction, agreement type), and feed both to search.
  - Replace or augment `MetadataExtractor` behind an interface.

- Reranking
  - After initial vector search, use an LLM or cross-encoder to rerank top results before answering.

- Summarization and chunking
  - Summarize long documents; generate semantic titles; dynamic chunking based on semantic boundaries.

- Safety and formatting
  - Add moderation, PII redaction, and answer style control via system prompts.

Implementation notes
- Existing `IEmbeddingService` makes it easy to swap local embeddings for API-based embeddings.
- Add a new endpoint (e.g., `/chat/ask`) for streaming answers; reuse SSE infra for token streaming.
- Cache answers and reranks keyed by (question, corpus version) to control costs.

## Handling large file uploads

Current behavior
- The upload endpoint reads the entire file into memory (`await file.read()`), then enqueues it. This is simple but not optimal for very large files.

Recommendations for large files
- Stream to disk or object storage
  - Use `UploadFile.file` to read in chunks and write to a temporary file or S3/GCS. Process from that path/URL in the background worker.
  - Consider `SpooledTemporaryFile` to keep small files in memory and spill large ones to disk.

- Increase resilience and backpressure
  - The upload queue is bounded; tune `queue.maxsize` in `UploadService` to match expected throughput.
  - Move heavy processing to a worker system (e.g., Celery/RQ) if concurrency grows.

- Chunked/resumable uploads
  - Add a client-side chunked upload (e.g., tus protocol) to support multi-GB files and resume on failure.
  - For browser uploads, consider direct-to-object-storage pre-signed URLs to bypass the app server.

- Parser and memory usage
  - Parse PDFs page-by-page where possible; avoid loading entire documents when the parser supports streaming.
  - Tune `TextChunker` window/overlap to control the number and size of embeddings.

- Database batching
  - Insert `DocumentChunk` rows in batches and commit periodically to keep transactions bounded.

- Limits and configuration
  - Expose max upload size and timeouts via env variables; return clear 413/408 errors when exceeded.
  - Validate supported types early to avoid wasted bandwidth.

Minimal code changes to move toward streaming
1) Replace `await file.read()` with chunked reads written to a temp file.
2) Pass a file path to the background worker; update `TextExtractor` to accept a path/stream.
3) Store the original file in object storage if long-term retention is needed; persist only metadata + derived text/embeddings in Postgres.

Tuning chunking size
```python
# dependencies.py
chunker=TextChunker(max_tokens=1000, overlap=200)  # Increase max_tokens for fewer, larger chunks
```
