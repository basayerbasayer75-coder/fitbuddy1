# FitBuddy – AI Fitness Plan Generator

Complete FastAPI + Jinja2 + SQLite + Gemini implementation based on the supplied FitBuddy PDF.

## Run

1. Open this folder in VS Code.
2. `python -m venv .venv`
3. Windows: `.venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`.
6. Add `GOOGLE_API_KEY=...` and set `DEMO_MODE=false` for real Gemini calls. Keep `DEMO_MODE=true` to test the complete UI/database without a key.
7. `uvicorn app.main:app --reload`
8. Open http://127.0.0.1:8000 and /docs.
9. Test with `pytest -q`.

The PDF names older Gemini 1.5 models and the older SDK. This implementation uses Google's current `google-genai` SDK and configurable model names so it is not hard-coded to an obsolete model.

## Structure

```text
FitBuddy/
  app/
    __init__.py database.py models.py schemas.py routes.py main.py
    gemini_generator.py gemini_flash_generator.py updated_plan.py
  templates/
    base.html index.html result.html all_users.html error.html
  static/style.css
  tests/test_app.py
  requirements.txt .env.example .gitignore README.md
```

FitBuddy is a wellness-planning demonstration, not a medical service.
