from fastapi import APIRouter,UploadFile,File,Depends,HTTPException
from app.core.security import get_current_user
from app.services.pdf_service import extract_text_from_pdf
from app.services.text_service import clean_resume_text
from sqlalchemy.orm import Session
from app.database.dependencies import get_db

from app.models.resume import Resume
from app.services.storage_service import (save_resume_file,delete_resume_file,)
from app.services.resume_ai_service import analyze_resume
from app.services.resume_service import (process_resume,ResumeExtractionError,ResumeAIError)

router=APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)

MAX_FILE_SIZE=5*1024*1024

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="File is empty",
        )

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB",
        )

    if not contents.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file",
        )

    try:
        resume = await process_resume(
            contents=contents,
            filename=file.filename,
            user_id=current_user.id,
            db=db,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except ResumeExtractionError as e:
        print(
            f"Resume extraction failed:{e}")

        raise HTTPException(
            status_code=400,
            detail="Unable to process the resume PDF.",
        )

    except ResumeAIError as e:
        print(f"Resume AI analysis failed:{e}")
        raise HTTPException(
            status_code=400,
            detail="AI analysis failed.please try again",
        )

    except exception as e:
        print(f"Resume processing failed:"
        f"{type(e).__name__}:{e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Resume processing failed"
        )

    return {
        "id": resume.id,
        "filename": resume.original_filename,
        "file_path": resume.file_path,
        "content_type": file.content_type,
        "size": len(contents),
        "text": resume.extracted_text,
        "ai_analysis": resume.ai_analysis,
        "status": resume.status,
        "user_id": resume.user_id,
        "created_at": resume.created_at,
        "updated_at": resume.updated_at,
    }

@router.get("/")
async def get_resumes(
    current_user=Depends(get_current_user),
    db:Session=Depends(get_db),
):
    resumes=(
        db.query(Resume)
        .filter(Resume.user_id==current_user.id)
        .all()
    )
    return resumes

@router.get("/{resume_id}/skills")
async def get_resume_skills(
    resume_id:int,
    current_user=Depends(get_current_user),
    db:Session=Depends(get_db),
):
    resume=(
        db.query(Resume)
        .filter(
            Resume.id==resume_id,
            Resume.user_id==current_user.id
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    if not resume.ai_analysis:
        raise HTTPException(
            status_code=404,
            detail="Ai analysis not available"
        )

    return{
        "resume_id":resume.id,
        "technical_skills":resume.ai_analysis.get(
            "technical_skills",[]
        ),
        "tools":resume.ai_analysis.get(
            "tools",[]
        ),
        "concepts":resume.ai_analysis.get(
            "concepts",[]
        ),

    }

@router.get("/{resume_id}")
async def get_resume(
    resume_id:int,
    current_user=Depends(get_current_user),
    db:Session=Depends(get_db)
):
    resume=(
        db.query(Resume)
        .filter(
            Resume.id==resume_id,
            Resume.user_id==current_user.id,
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )
    return resume

@router.delete("/{resume_id}")
async def delete_resume(
    resume_id:int,
    current_user=Depends(get_current_user),
    db:Session=Depends(get_db)
):
    resume=(
        db.query(Resume)
        .filter(
            Resume.id==resume_id,
            Resume.user_id==current_user.id,
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    file_path=resume.file_path

    db.delete(resume)
    db.commit()

    delete_resume_file(file_path)
    return {
        "message":"Resume deleted successfully"
    }

