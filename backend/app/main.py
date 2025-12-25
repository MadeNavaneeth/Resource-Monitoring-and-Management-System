from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.database import engine, Base

# Import models so SQLAlchemy registers them with Base
from app.models import models

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resource Monitoring System API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Rate Limiting middleware
from app.core.rate_limiter import rate_limit_middleware
app.middleware("http")(rate_limit_middleware)

from app.api import endpoints, auth

app.include_router(endpoints.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Resource Monitoring System API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# --- Discovery Beacon ---
from app.core.discovery import ServiceBeacon
from app.core.cleanup import MetricCleaner

beacon = ServiceBeacon()
cleaner = MetricCleaner()

@app.on_event("startup")
async def startup_event():
    beacon.start()
    cleaner.start()

@app.on_event("shutdown")
async def shutdown_event():
    beacon.stop()
    cleaner.stop()
