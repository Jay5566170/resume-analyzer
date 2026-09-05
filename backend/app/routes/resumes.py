from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
import json
from datetime import datetime

from ..database import get_db
from ..models import Resume
from ..schemas import ResumeResponse
from ..utils.pdf_parser import extract_text
from ..utils.ai_analyzer import analyze_resume_with_ai  # ✅ THIS IS THE CORRECT IMPORT

router = APIRouter(prefix="/resumes", tags=["resumes"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def analyze_resume_background(resume_id: int, file_path: str, db: Session):
    """Background task to analyze a resume."""
    try:
        print(f"🔍 Background analysis started for resume ID: {resume_id}")
        
        text = extract_text(file_path)
        if not text:
            print(f"❌ No text extracted from file: {file_path}")
            return
        
        analysis = analyze_resume_with_ai(text)
        
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if resume:
            resume.name = analysis.get("name")
            resume.email = analysis.get("email")
            resume.phone = analysis.get("phone")
            resume.skills = json.dumps(analysis.get("skills", []))
            resume.experience = json.dumps(analysis.get("experience", []))
            resume.education = json.dumps(analysis.get("education", []))
            resume.summary = analysis.get("summary")
            db.commit()
            print(f"✅ Background analysis complete for resume ID: {resume_id}")
        else:
            print(f"❌ Resume not found for ID: {resume_id}")
            
    except Exception as e:
        print(f"❌ Background analysis failed: {e}")


@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files allowed")
    
    timestamp = int(datetime.now().timestamp())
    file_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    db_resume = Resume(
        filename=file.filename,
        file_path=file_path
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    if background_tasks:
        background_tasks.add_task(analyze_resume_background, db_resume.id, file_path, db)
        print(f"⏳ Background analysis scheduled for resume ID: {db_resume.id}")
    
    return db_resume


@router.post("/analyze/{resume_id}", response_model=ResumeResponse)
def analyze_resume_now(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    print(f"🔍 Starting analysis for resume ID: {resume_id}")
    
    text = extract_text(resume.file_path)
    if not text:
        resume.summary = "Could not extract text from file"
        db.commit()
        return resume
    
    analysis = analyze_resume_with_ai(text)
    
    resume.name = analysis.get("name")
    resume.email = analysis.get("email")
    resume.phone = analysis.get("phone")
    resume.skills = json.dumps(analysis.get("skills", []))
    resume.experience = json.dumps(analysis.get("experience", []))
    resume.education = json.dumps(analysis.get("education", []))
    resume.summary = analysis.get("summary")
    db.commit()
    db.refresh(resume)
    
    print(f"✅ Analysis complete for resume ID: {resume_id}")
    return resume


@router.get("/", response_model=List[ResumeResponse])
def get_all_resumes(db: Session = Depends(get_db)):
    return db.query(Resume).all()


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.delete("/{resume_id}")
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)
    
    db.delete(resume)
    db.commit()
    return {"message": f"Resume {resume_id} deleted successfully"}


@router.get("/search/", response_model=List[ResumeResponse])
def search_resumes(q: str, db: Session = Depends(get_db)):
    results = db.query(Resume).filter(
        (Resume.name.ilike(f"%{q}%")) |
        (Resume.email.ilike(f"%{q}%")) |
        (Resume.skills.ilike(f"%{q}%"))
    ).all()
    return results