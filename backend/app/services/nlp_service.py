import re
from functools import lru_cache

import spacy

from app.utils.constants import EDUCATION_KEYWORDS, EXPERIENCE_KEYWORDS, TECH_SKILLS


@lru_cache
def get_nlp_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        return spacy.blank("en")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def extract_skills(text: str) -> list[str]:
    normalized = normalize_text(text)
    found: set[str] = set()
    for skill in TECH_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, normalized):
            found.add(skill)

    # If the full model is available, include noun chunks that match skill-like compounds.
    nlp = get_nlp_model()
    if "parser" in nlp.pipe_names:
        doc = nlp(text)
        for chunk in doc.noun_chunks:
            value = chunk.text.lower().strip()
            if value in TECH_SKILLS:
                found.add(value)

    return sorted(found)


def extract_experience_years(text: str) -> int:
    normalized = normalize_text(text)
    years = re.findall(r"(\d{1,2})\+?\s+years?", normalized)
    if not years:
        return 0
    return max(int(y) for y in years)


def has_education_section(text: str) -> bool:
    normalized = normalize_text(text)
    return any(keyword in normalized for keyword in EDUCATION_KEYWORDS)


def has_experience_section(text: str) -> bool:
    normalized = normalize_text(text)
    return any(keyword in normalized for keyword in EXPERIENCE_KEYWORDS)


def extract_keywords(text: str) -> list[str]:
    return extract_skills(text)
