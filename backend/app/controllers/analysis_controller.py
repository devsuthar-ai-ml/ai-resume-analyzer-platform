from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.analysis_result import AnalysisResult
from app.models.job_description import JobDescription
from app.models.resume import Resume
from app.models.user import User
from app.schemas.analysis import AnalysisDetailResponse, AnalysisResponse, AnalyzeRequest, ScoreBreakdown
from app.services.analysis_service import run_analysis


def analyze_resume(payload: AnalyzeRequest, current_user: User, db: Session) -> AnalysisResponse:
    resume = (
        db.query(Resume)
        .filter(Resume.id == payload.resume_id, Resume.user_id == current_user.id)
        .first()
    )
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    job_description = JobDescription(
        user_id=current_user.id,
        title=payload.job_title,
        content=payload.job_description,
    )
    db.add(job_description)
    db.flush()

    computed = run_analysis(resume.extracted_text, payload.job_description)

    result = AnalysisResult(
        user_id=current_user.id,
        resume_id=resume.id,
        job_description_id=job_description.id,
        match_percentage=computed.match_percentage,
        resume_score=computed.resume_score,
        detected_skills=computed.detected_skills,
        missing_skills=computed.missing_skills,
        suggestions=computed.suggestions,
        score_breakdown=computed.score_breakdown,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    return AnalysisResponse(
        id=result.id,
        resume_id=result.resume_id,
        job_description_id=result.job_description_id,
        match_percentage=result.match_percentage,
        resume_score=result.resume_score,
        detected_skills=result.detected_skills,
        missing_skills=result.missing_skills,
        suggestions=result.suggestions,
        score_breakdown=ScoreBreakdown(**result.score_breakdown),
        created_at=result.created_at,
    )


def get_analysis_result(result_id: int, current_user: User, db: Session) -> AnalysisDetailResponse:
    result = (
        db.query(AnalysisResult)
        .filter(AnalysisResult.id == result_id, AnalysisResult.user_id == current_user.id)
        .first()
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis result not found")
    return AnalysisDetailResponse.model_validate(result)
