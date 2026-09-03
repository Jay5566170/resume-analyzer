from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
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
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}