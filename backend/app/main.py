# app/main.py
from fastapi import FastAPI
from app.db import init_db
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(upload.router)
app.include_router(query.router)
app.include_router(dashboard.router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()