"""
Keyword analysis service.
Extracts keywords from job descriptions, detects skills in resumes,
computes match scores, and generates improvement suggestions.
"""

import re
import logging
from typing import List, Set

from app.config import TECH_SKILLS, SKILL_SUGGESTIONS

logger = logging.getLogger(__name__)


def normalize_text(text: str) -> str:
    """Lowercase and normalize whitespace in text."""
    text = text.lower()
    text = re.sub(r"[^\w\s./+-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_keywords_from_job_description(job_description: str) -> List[str]:
    """
    Extract recognized tech skills from a job description.

    Scans the job description for any skills present in the TECH_SKILLS list.
    Multi-word skills (e.g. 'machine learning') are matched as phrases.

    Args:
        job_description: Raw job description text.

    Returns:
        Sorted list of unique skill keywords found in the job description.
    """
    normalized = normalize_text(job_description)
    found: Set[str] = set()

    for skill in TECH_SKILLS:
        # Use word-boundary matching for single-word skills,
        # phrase matching for multi-word skills
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, normalized):
            # Normalize ci/cd alias
            canonical = "ci/cd" if skill == "cicd" else skill
            found.add(canonical)

    return sorted(found)


def detect_skills_in_resume(resume_text: str) -> List[str]:
    """
    Detect tech skills present in the resume text.

    Args:
        resume_text: Extracted plain text from the resume.

    Returns:
        Sorted list of unique skills found in the resume.
    """
    normalized = normalize_text(resume_text)
    found: Set[str] = set()

    for skill in TECH_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, normalized):
            canonical = "ci/cd" if skill == "cicd" else skill
            found.add(canonical)

    return sorted(found)


def compute_match_score(required_keywords: List[str], found_skills: List[str]) -> float:
    """
    Compute the match score as a percentage.

    Score = (matched keywords / required keywords) × 100

    Args:
        required_keywords: Skills extracted from the job description.
        found_skills: Skills detected in the resume.

    Returns:
        Float between 0.0 and 100.0 representing the match percentage.
    """
    if not required_keywords:
        return 0.0

    required_set = set(required_keywords)
    found_set = set(found_skills)
    matched = required_set & found_set
    score = (len(matched) / len(required_set)) * 100
    return round(score, 1)


def get_missing_keywords(required_keywords: List[str], found_skills: List[str]) -> List[str]:
    """
    Return keywords required by the job but absent from the resume.

    Args:
        required_keywords: Skills from the job description.
        found_skills: Skills found in the resume.

    Returns:
        Sorted list of missing skill keywords.
    """
    required_set = set(required_keywords)
    found_set = set(found_skills)
    return sorted(required_set - found_set)


def generate_suggestions(missing_keywords: List[str]) -> List[str]:
    """
    Generate actionable improvement suggestions for missing keywords.

    Args:
        missing_keywords: Skills that are required but missing from the resume.

    Returns:
        List of suggestion strings.
    """
    suggestions = []
    for keyword in missing_keywords:
        suggestion = SKILL_SUGGESTIONS.get(keyword)
        if suggestion:
            suggestions.append(suggestion)
        else:
            suggestions.append(
                f"Consider adding '{keyword.title()}' to your resume through "
                f"projects, courses, or certifications."
            )
    return suggestions


def get_score_label(score: float) -> dict:
    """
    Return a human-readable label and color class for a given score.

    Args:
        score: Match percentage (0–100).

    Returns:
        Dict with 'label' and 'color' keys.
    """
    if score >= 80:
        return {"label": "Excellent Match", "color": "success"}
    elif score >= 60:
        return {"label": "Good Match", "color": "info"}
    elif score >= 40:
        return {"label": "Partial Match", "color": "warning"}
    else:
        return {"label": "Low Match", "color": "danger"}
