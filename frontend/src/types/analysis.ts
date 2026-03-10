export interface AnalyzePayload {
  resume_id: number;
  job_title: string;
  job_description: string;
}

export interface ScoreBreakdown {
  skill_coverage: number;
  semantic_similarity: number;
  experience_strength: number;
  education_strength: number;
}

export interface AnalysisResult {
  id: number;
  resume_id: number;
  job_description_id: number;
  match_percentage: number;
  resume_score: number;
  detected_skills: string[];
  missing_skills: string[];
  suggestions: string[];
  score_breakdown: ScoreBreakdown;
  created_at: string;
}
