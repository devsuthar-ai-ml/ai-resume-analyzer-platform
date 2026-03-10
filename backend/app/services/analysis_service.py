from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services import nlp_service


@dataclass
class AnalysisComputation:
    detected_skills: list[str]
    missing_skills: list[str]
    suggestions: list[str]
    match_percentage: float
    resume_score: int
    score_breakdown: dict[str, int]


def _semantic_similarity(text_a: str, text_b: str) -> float:
    if not text_a.strip() or not text_b.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        matrix = vectorizer.fit_transform([text_a, text_b])
        score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return float(max(score, 0.0))
    except ValueError:
        return 0.0


def run_analysis(resume_text: str, job_description: str) -> AnalysisComputation:
    resume_skills = nlp_service.extract_skills(resume_text)
    required_skills = nlp_service.extract_keywords(job_description)

    resume_skill_set = set(skill.lower() for skill in resume_skills)
    required_skill_set = set(skill.lower() for skill in required_skills)

    overlap = resume_skill_set.intersection(required_skill_set)
    missing = sorted(required_skill_set.difference(resume_skill_set))

    skill_coverage = (len(overlap) / len(required_skill_set) * 100.0) if required_skill_set else 0.0
    semantic_similarity = _semantic_similarity(resume_text, job_description) * 100.0

    experience_years = nlp_service.extract_experience_years(resume_text)
    experience_section = nlp_service.has_experience_section(resume_text)
    education_section = nlp_service.has_education_section(resume_text)

    experience_strength = min(experience_years * 15, 100)
    if experience_section and experience_strength < 40:
        experience_strength = 40
    education_strength = 100 if education_section else 30

    match_percentage = round((0.65 * skill_coverage) + (0.35 * semantic_similarity), 2)

    score_breakdown = {
        "skill_coverage": int(round(skill_coverage)),
        "semantic_similarity": int(round(semantic_similarity)),
        "experience_strength": int(round(experience_strength)),
        "education_strength": int(round(education_strength)),
    }

    resume_score = int(
        round(
            (score_breakdown["skill_coverage"] * 0.4)
            + (score_breakdown["semantic_similarity"] * 0.25)
            + (score_breakdown["experience_strength"] * 0.2)
            + (score_breakdown["education_strength"] * 0.15)
        )
    )
    resume_score = max(0, min(resume_score, 100))

    suggestions: list[str] = []
    if missing:
        suggestions.append("Add measurable evidence for missing skills: " + ", ".join(missing[:8]))
    if score_breakdown["semantic_similarity"] < 55:
        suggestions.append("Align resume wording with job description keywords and responsibilities.")
    if score_breakdown["experience_strength"] < 50:
        suggestions.append("Expand experience bullets with outcomes, impact metrics, and ownership scope.")
    if score_breakdown["education_strength"] < 60:
        suggestions.append("Include education details or relevant certifications to strengthen profile credibility.")
    if not suggestions:
        suggestions.append("Resume is well aligned. Focus on quantifiable achievements to further improve conversion.")

    return AnalysisComputation(
        detected_skills=sorted(resume_skill_set),
        missing_skills=missing,
        suggestions=suggestions,
        match_percentage=match_percentage,
        resume_score=resume_score,
        score_breakdown=score_breakdown,
    )
