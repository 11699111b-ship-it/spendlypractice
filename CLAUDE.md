# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup (first time)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the app
python3 app.py          # serves at http://127.0.0.1:5001

# Run tests
pytest                  # all tests
pytest tests/test_auth.py  # single file (once tests exist)
```

Always activate the venv before running anything: `source venv/bin/activate`.

## Project

**Spendly** — a step-by-step practice project for building a Flask expense tracker. The codebase is a scaffold; features are added one step at a time.

**Stack:** Python · Flask 3.1 · SQLite · Jinja2 · Werkzeug · pytest + pytest-flask

## Architecture

```
app.py              ← all routes; entry point
database/db.py      ← SQLite helpers: get_db(), init_db(), seed_db() (stub — students implement)
templates/
  base.html         ← shared layout (nav + footer); all pages extend this
  landing.html      ← homepage (YouTube modal, hero, etc.)
  login.html / register.html / terms.html / privacy.html
static/
  css/style.css     ← app-wide styles
  css/landing.css   ← landing-page-only styles
  js/main.js        ← frontend interactivity
```

**Request flow:** browser → `app.py` route → `render_template()` → Jinja2 fills `base.html` + child template → response.

## Implementation roadmap (placeholder routes)

Routes in `app.py` marked "coming in Step N" are intentional stubs:

| Route | Step |
|---|---|
| `/logout` | Step 3 |
| `/profile` | Step 4 |
| `/expenses/add` | Step 7 |
| `/expenses/<id>/edit` | Step 8 |
| `/expenses/<id>/delete` | Step 9 |

`database/db.py` is also a stub — the comment there lists exactly what to implement (`get_db`, `init_db`, `seed_db`).
