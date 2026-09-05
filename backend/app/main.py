from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text  # ← ADDED THIS
from .database import engine, Base, get_db
from . import models
from .routes import resumes

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Resume Analyzer API",
    description="Upload, analyze, and manage resumes with AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resumes.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Resume Analyzer API!",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # ✅ FIXED: Using text() for raw SQL
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}