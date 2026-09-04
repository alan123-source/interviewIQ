from sqlalchemy.orm import Session

from app.models.resume import Resume

from app.services.storage_service import (
    save_resume_file,
    delete_resume_file,
)

from app.services.pdf_service import extract_text_from_pdf
from app.services.text_service import clean_resume_text
from app.services.resume_ai_service import analyze_resume
from app.database.db import SessionLocal
from sqlalchemy.exc import SQLAlchemyError


class ResumeProcessingError(Exception):
    """Base error for resume processing failures."""
    pass


class ResumeExtractionError(ResumeProcessingError):
    """Raised when PDF text extraction fails."""
    pass


class ResumeAIError(ResumeProcessingError):
    """Raised when AI analysis fails."""
    pass

async def process_resume(
    contents: bytes,
    filename: str,
    user_id: int,
    db: Session,
):
    # 1. Save the uploaded file
    file_path = save_resume_file(
        contents,
        filename
    )

    try:
        # 2. Extract text from PDF
        raw_text = extract_text_from_pdf(contents)

    except ValueError as exc:
        delete_resume_file(file_path)
        raise ResumeExtractionError(
            "Unable to extract text from resume PDF"
        ) from exc

    # 3. Clean extracted text
    text = clean_resume_text(raw_text)

    # 4. Make sure enough text was extracted
    if len(text.strip()) < 50:
        delete_resume_file(file_path)
        raise ValueError(
            "Could not extract enough text from this PDF"
        )

    try:
        # 5. Analyze resume using AI
        ai_result =  analyze_resume(text)

    except Exception as exc:
        delete_resume_file(file_path)
        raise ResumeAIError(
            "Resume AI analysis failed"
        ) from exc

    # 6. Create database record
    resume = Resume(
        user_id=user_id,
        original_filename=filename,
        file_path=file_path,
        extracted_text=text,
        ai_analysis=ai_result.model_dump(),
        status="completed",
    )
    
    try:

        db.add(resume)
        db.commit()
        db.refresh(resume)
    except SQLAlchemyError as exc:
        db.rollback()
        delete_resume_file(file_path)

        print(
            f"Resume database Error"
            f"{type(exc).__name__}:{exc}"
        )

        raise ResumeProcessingError(
            "Failed to save resume"
        ) from exc
    return resume

