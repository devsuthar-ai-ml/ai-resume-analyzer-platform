from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AnalyzeRequest(BaseModel):
    resume_id: int = Field(gt=0)
    job_title: str = Field(min_length=2, max_length=255)
    job_description: str = Field(min_length=20)


class ScoreBreakdown(BaseModel):
    skill_coverage: int
    semantic_similarity: int
    experience_strength: int
    education_strength: int


class AnalysisResponse(BaseModel):
    id: int
    resume_id: int
    job_description_id: int
    match_percentage: float
    resume_score: int
    detected_skills: list[str]
    missing_skills: list[str]
    suggestions: list[str]
    score_breakdown: ScoreBreakdown
    created_at: datetime


class AnalysisDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    resume_id: int
    job_description_id: int
    match_percentage: float
    resume_score: int
    detected_skills: list[str]
    missing_skills: list[str]
    suggestions: list[str]
    score_breakdown: dict
    created_at: datetime
