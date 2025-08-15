# app/main.py
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread

app = FastAPI(title="FastAPI React Starter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routes.controllers import upload
from app.routes.controllers import query, dashboard
from app.routes.controllers import notifications

# Central API router with /api prefix
api = APIRouter(prefix="/api")
api.include_router(upload.router)
api.include_router(query.router)
api.include_router(dashboard.router)
api.include_router(notifications.router)

app.include_router(api)


@app.on_event("startup")
def _warm_background_services() -> None:
    # Warm the embedding model in a background thread so startup is not blocked
    def _warm() -> None:
        try:
            from app.dependencies import get_embedding_service
            svc = get_embedding_service()
            # Access dimension which triggers lazy load in LocalEmbeddingService
            _ = svc.dimension()
        except Exception:
            # Best-effort warmup; failures shouldn't block the app
            pass

    Thread(target=_warm, daemon=True).start()
