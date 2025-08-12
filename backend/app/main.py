# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.controllers import health, greeting

app = FastAPI(title="FastAPI React Starter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apply a common API prefix here (e.g., for versioning: "/api/v1")
app.include_router(health.router, prefix="/api")
app.include_router(greeting.router, prefix="/api")