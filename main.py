"""
Application entry point.
Run with: uvicorn main:app --reload
"""

from app.main import app  # noqa: F401 — re-exported for uvicorn

__all__ = ["app"]
