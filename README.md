# Resume Keyword Analyzer

A clean, production-ready web app built with **FastAPI** that analyzes a resume against a job description and returns:

- **Match Score (%)** — how well the resume aligns with the job
- **Found Skills** — tech skills detected in the resume
- **Missing Keywords** — required skills absent from the resume
- **Improvement Suggestions** — actionable advice for each gap

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Python 3.11+ |
| PDF Parsing | pdfplumber |
| DOCX Parsing | python-docx |
| Templating | Jinja2 |
| Frontend | Vanilla JS, CSS (no framework) |
| Server | Uvicorn (ASGI) |

---

## Project Structure

```
resume-keyword-analyzer/
├── app/
│   ├── __init__.py
│   ├── main.py              # App factory, middleware, router registration
│   ├── config.py            # Skills list, suggestions, constants
│   ├── models.py            # Pydantic request/response schemas
│   ├── routers/
│   │   ├── api.py           # POST /api/analyze endpoint
│   │   └── pages.py         # HTML page routes (/, /analyzer, /results)
│   ├── services/
│   │   ├── file_parser.py   # PDF & DOCX text extraction
│   │   └── keyword_analyzer.py  # Keyword matching & scoring logic
│   ├── static/
│   │   └── css/style.css    # Global styles
│   └── templates/
│       ├── base.html        # Shared layout (navbar, footer)
│       ├── home.html        # Landing page
│       ├── analyzer.html    # Upload form page
│       └── results.html     # Results display page
├── main.py                  # Uvicorn entry point
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Clone & install dependencies

```bash
git clone <repo-url>
cd resume-keyword-analyzer

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Run the development server

```bash
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

### 3. API Docs

Interactive Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Reference

### `POST /api/analyze`

Analyze a resume against a job description.

**Request** — `multipart/form-data`

| Field | Type | Description |
|-------|------|-------------|
| `resume` | File | PDF or DOCX resume (max 10 MB) |
| `job_description` | string | Full job description text |

**Response** — `200 OK`

```json
{
  "match_score": 75.0,
  "score_label": "Good Match",
  "score_color": "info",
  "required_keywords": ["python", "docker", "aws"],
  "found_skills": ["python", "docker", "git"],
  "matched_keywords": ["python", "docker"],
  "missing_keywords": ["aws"],
  "suggestions": ["Consider adding 'Aws' to your resume through projects, courses, or certifications."],
  "resume_filename": "my_resume.pdf"
}
```

---

## Keyword Logic

1. Normalize both texts (lowercase, strip punctuation)
2. Scan job description for skills from the predefined `TECH_SKILLS` list
3. Scan resume text for the same skills
4. Compute: `score = (matched / required) × 100`
5. Generate suggestions for each missing skill

---

## Skills Analyzed

Python, FastAPI, Flask, Django, SQL, PostgreSQL, Docker, Kubernetes, AWS, Azure, Git, Linux, React, Angular, CI/CD, JavaScript, TypeScript, Node.js, MongoDB, Redis, Elasticsearch, GraphQL, Terraform, Jenkins, Pandas, NumPy, Machine Learning, and more.

---

## Production Notes

- Swap `allow_origins=["*"]` in CORS middleware with your actual domain
- Add rate limiting (e.g., `slowapi`) for public deployments
- Store uploaded files in S3 or similar instead of memory for scale
- Add authentication if exposing sensitive resume data
