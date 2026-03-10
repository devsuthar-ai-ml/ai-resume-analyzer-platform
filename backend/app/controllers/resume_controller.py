import os

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeHistoryResponse, ResumeUploadResponse
from app.services.file_parser_service import extract_text
from app.utils.file_utils import generate_stored_filename, validate_upload_file


def upload_resume(file: UploadFile, current_user: User, db: Session) -> ResumeUploadResponse:
    content = file.file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file")

    validate_upload_file(file, len(content))
    extension = os.path.splitext(file.filename or "")[1].lower()

    try:
        extracted_text = extract_text(content, extension)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to parse resume file") from exc

    if not extracted_text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No readable text found in resume")

    resume = Resume(
        user_id=current_user.id,
        filename=generate_stored_filename(file.filename or "resume"),
        original_filename=file.filename or "resume",
        file_type=extension,
        file_size=len(content),
        extracted_text=extracted_text,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return ResumeUploadResponse(
        id=resume.id,
        filename=resume.filename,
        original_filename=resume.original_filename,
        file_type=resume.file_type,
        file_size=resume.file_size,
        created_at=resume.created_at,
    )


def get_resume_history(current_user: User, db: Session) -> ResumeHistoryResponse:
    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .all()
    )
    return ResumeHistoryResponse(items=resumes)
