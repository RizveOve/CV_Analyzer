"""
Resume Keyword Analyzer — FastAPI application entry point.
"""

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import api, pages

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_app() -> FastAPI:
    app = FastAPI(
        title="Resume Keyword Analyzer",
        description=(
            "Upload a resume (PDF/DOCX) and paste a job description. "
            "The app extracts text, compares keywords, and returns a match score, "
            "found skills, missing keywords, and improvement suggestions."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # --- CORS (permissive for local dev; tighten for production) ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    # --- Static files ---
    static_dir = Path("app/static")
    static_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # --- Routers ---
    app.include_router(pages.router)
    app.include_router(api.router)

    @app.on_event("startup")
    async def startup_event():
        logger.info("Resume Keyword Analyzer started successfully.")

    return app


app = create_app()
