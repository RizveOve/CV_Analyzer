"""
Pydantic models for request/response schemas.
"""

from typing import List
from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    """Full analysis result returned to the client."""

    match_score: float = Field(..., description="Match percentage (0–100)", ge=0, le=100)
    score_label: str = Field(..., description="Human-readable score label")
    score_color: str = Field(..., description="Bootstrap color class for the score badge")
    required_keywords: List[str] = Field(..., description="Skills extracted from the job description")
    found_skills: List[str] = Field(..., description="Skills detected in the resume")
    matched_keywords: List[str] = Field(..., description="Skills present in both resume and job description")
    missing_keywords: List[str] = Field(..., description="Skills required but absent from the resume")
    suggestions: List[str] = Field(..., description="Actionable improvement suggestions")
    resume_filename: str = Field(..., description="Original uploaded filename")

    class Config:
        json_schema_extra = {
            "example": {
                "match_score": 75.0,
                "score_label": "Good Match",
                "score_color": "info",
                "required_keywords": ["python", "docker", "aws"],
                "found_skills": ["python", "docker", "git"],
                "matched_keywords": ["python", "docker"],
                "missing_keywords": ["aws"],
                "suggestions": ["Consider adding 'Aws' to your resume through projects, courses, or certifications."],
                "resume_filename": "my_resume.pdf",
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response."""

    detail: str = Field(..., description="Error message")
