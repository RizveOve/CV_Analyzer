"""
Page routes — serve HTML templates for the three UI pages.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, summary="Home page")
async def home(request: Request):
    """Render the landing / home page."""
    return templates.TemplateResponse(request, "home.html")


@router.get("/analyzer", response_class=HTMLResponse, summary="Analyzer page")
async def analyzer(request: Request):
    """Render the resume upload and job description input page."""
    return templates.TemplateResponse(request, "analyzer.html")


@router.get("/results", response_class=HTMLResponse, summary="Results page")
async def results(request: Request):
    """
    Render the results page shell.
    Actual results are populated via the /api/analyze endpoint.
    """
    return templates.TemplateResponse(request, "results.html")


@router.get("/", response_class=HTMLResponse, summary="Home page")
async def home(request: Request):
    """Render the landing / home page."""
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/analyzer", response_class=HTMLResponse, summary="Analyzer page")
async def analyzer(request: Request):
    """Render the resume upload and job description input page."""
    return templates.TemplateResponse("analyzer.html", {"request": request})


@router.get("/results", response_class=HTMLResponse, summary="Results page")
async def results(request: Request):
    """
    Render the results page shell.
    Actual results are populated via the /api/analyze endpoint.
    """
    return templates.TemplateResponse("results.html", {"request": request})
