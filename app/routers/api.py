"""
API routes — handle resume upload and analysis.
"""

import logging
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB
from app.models import AnalysisResult
from app.services.file_parser import extract_text
from app.services.keyword_analyzer import (
    compute_match_score,
    detect_skills_in_resume,
    extract_keywords_from_job_description,
    generate_suggestions,
    get_missing_keywords,
    get_score_label,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Analysis"])

MAX_FILE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


@router.post(
    "/analyze",
    response_model=AnalysisResult,
    summary="Analyze resume against job description",
    responses={
        400: {"description": "Invalid file type, file too large, or empty job description"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error during analysis"},
    },
)
async def analyze_resume(
    resume: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    job_description: str = Form(..., description="Job description text"),
) -> AnalysisResult:
    """
    Upload a resume and provide a job description to receive:
    - Match score (%)
    - Found skills
    - Missing keywords
    - Improvement suggestions
    """
    # --- Validate file extension ---
    suffix = Path(resume.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{suffix}'. Please upload a PDF or DOCX file.",
        )

    # --- Validate job description ---
    job_description = job_description.strip()
    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description cannot be empty.",
        )

    # --- Read and validate file size ---
    file_bytes = await resume.read()
    if len(file_bytes) > MAX_FILE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds the {MAX_FILE_SIZE_MB} MB limit.",
        )
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    # --- Extract text from resume ---
    try:
        resume_text = extract_text(file_bytes, resume.filename or "resume")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected error parsing resume: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while reading the resume.",
        ) from exc

    # --- Perform keyword analysis ---
    required_keywords = extract_keywords_from_job_description(job_description)
    found_skills = detect_skills_in_resume(resume_text)
    matched_keywords = sorted(set(required_keywords) & set(found_skills))
    missing_keywords = get_missing_keywords(required_keywords, found_skills)
    match_score = compute_match_score(required_keywords, found_skills)
    suggestions = generate_suggestions(missing_keywords)
    score_meta = get_score_label(match_score)

    logger.info(
        "Analysis complete | file=%s | score=%.1f%% | matched=%d/%d",
        resume.filename,
        match_score,
        len(matched_keywords),
        len(required_keywords),
    )

    return AnalysisResult(
        match_score=match_score,
        score_label=score_meta["label"],
        score_color=score_meta["color"],
        required_keywords=required_keywords,
        found_skills=found_skills,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        suggestions=suggestions,
        resume_filename=resume.filename or "resume",
    )
