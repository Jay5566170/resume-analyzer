from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime

from ..database import get_db
from ..models import Resume
from ..schemas import ResumeResponse

router = APIRouter(prefix="/resumes", tags=["resumes"])

# Upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a resume file and create a database entry."""
    
    # Validate file type
    if not file.filename.endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files allowed")
    
    # Save file
    timestamp = int(datetime.now().timestamp())
    file_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create database entry
    db_resume = Resume(
        filename=file.filename,
        file_path=file_path
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    return db_resume

@router.get("/", response_model=List[ResumeResponse])
def get_all_resumes(db: Session = Depends(get_db)):
    """Get all resumes."""
    return db.query(Resume).all()

@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """Get a specific resume by ID."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.delete("/{resume_id}")
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    """Delete a resume."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Delete file
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)
    
    db.delete(resume)
    db.commit()
    return {"message": f"Resume {resume_id} deleted successfully"}