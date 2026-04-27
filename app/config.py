"""
Application configuration and constants.
"""

# Predefined tech skills list
TECH_SKILLS = [
    "python", "fastapi", "flask", "django", "sql", "postgresql",
    "docker", "kubernetes", "aws", "azure", "git", "linux",
    "react", "angular", "ci/cd", "cicd",
    # Extended skills for richer analysis
    "javascript", "typescript", "node.js", "nodejs", "mongodb",
    "redis", "elasticsearch", "graphql", "rest", "restful",
    "microservices", "terraform", "jenkins", "github actions",
    "pytest", "unittest", "celery", "rabbitmq", "kafka",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "machine learning", "deep learning", "nlp", "data science",
    "html", "css", "sass", "webpack", "vue", "vue.js",
    "java", "spring", "c++", "c#", "go", "golang", "rust",
    "bash", "shell", "powershell", "ansible", "nginx", "apache",
    "mysql", "sqlite", "oracle", "dynamodb", "firebase",
    "oauth", "jwt", "ssl", "tls", "agile", "scrum", "devops",
]

# Improvement suggestions mapped to missing skill categories
SKILL_SUGGESTIONS = {
    "python": "Add Python projects or certifications to your resume.",
    "fastapi": "Mention FastAPI experience in your projects section.",
    "flask": "Include Flask-based projects or APIs you've built.",
    "django": "Highlight Django projects, especially REST APIs with DRF.",
    "sql": "Showcase SQL skills with query examples or database projects.",
    "postgresql": "Mention PostgreSQL in your database experience section.",
    "docker": "Add Docker containerization experience or personal projects.",
    "kubernetes": "Include Kubernetes orchestration skills or certifications (CKA).",
    "aws": "Consider AWS certifications (Cloud Practitioner, Solutions Architect).",
    "azure": "Add Azure experience or pursue AZ-900 certification.",
    "git": "Ensure your GitHub profile is linked and active.",
    "linux": "Mention Linux administration or shell scripting experience.",
    "react": "Add React projects to your portfolio or GitHub.",
    "angular": "Include Angular projects or mention component-based UI experience.",
    "ci/cd": "Describe CI/CD pipelines you've set up (GitHub Actions, Jenkins).",
    "javascript": "Showcase JavaScript projects or frameworks you've used.",
    "typescript": "Mention TypeScript usage in frontend or backend projects.",
    "machine learning": "Add ML projects, Kaggle competitions, or relevant courses.",
    "devops": "Highlight DevOps practices: automation, monitoring, deployment.",
    "agile": "Mention Agile/Scrum methodology experience in your work history.",
}

# File upload settings
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
UPLOAD_DIR = "uploads"
