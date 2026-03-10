from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.controllers.resume_controller import get_resume_history, upload_resume
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.resume import ResumeHistoryResponse, ResumeUploadResponse

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
def upload(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return upload_resume(file, current_user, db)


@router.get("/history", response_model=ResumeHistoryResponse)
def history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_resume_history(current_user, db)
