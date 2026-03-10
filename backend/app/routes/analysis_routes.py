from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.analysis_controller import analyze_resume, get_analysis_result
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.analysis import AnalysisDetailResponse, AnalysisResponse, AnalyzeRequest

router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=AnalysisResponse)
def analyze(
    payload: AnalyzeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return analyze_resume(payload, current_user, db)


@router.get("/results/{result_id}", response_model=AnalysisDetailResponse)
def get_result(
    result_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_analysis_result(result_id, current_user, db)
