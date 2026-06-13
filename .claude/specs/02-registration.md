# Spec: Registration

## Overview
Wire up the `/register` route to accept POST submissions, validate the form, hash the password, and insert the new user into the database. On success, the user is redirected to `/login`. On failure, the form re-renders with an inline error message. This is the first feature where the app accepts user input and writes to the database.

## Depends on
- Step 1 (Database Setup) — `get_db()`, `init_db()`, `users` table must exist.

## Routes
- `GET /register` — renders the registration form — public (already exists, keep as-is)
- `POST /register` — processes form submission — publi/c

## Database changes
No new tables or columns. The `users` table from Step 1 covers all fields needed:
- `name` TEXT NOT NULL
- `email` TEXT UNIQUE NOT NULL
- `password_hash` TEXT NOT NULL

## Templates
- **Modify:** `templates/register.html` — already has `{% if error %}` block and correct form fields; no template changes needed unless the form action or field names differ from what the route expects. Verify field names match: `name`, `email`, `password`.

## Files to change
- `app.py` — add POST handler to `/register` route; add `app.secret_key`; add imports for `request`, `redirect`, `url_for`, `session`

## Files to create
None.

## New dependencies
No new pip packages.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` via `get_db()` only
- Parameterised queries only — never string-format SQL
- Hash passwords with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values (no template changes required here)
- All templates extend `base.html` (already satisfied)
- Set `app.secret_key` to a hard-coded dev string (e.g. `"dev-secret-change-in-prod"`) — do not use env vars yet
- Validation order: check all fields non-empty → check password length ≥ 8 → attempt insert → catch duplicate email
- Catch the duplicate email via `sqlite3.IntegrityError`, not a pre-query SELECT
- After successful registration, redirect to `/login` — do NOT auto-login the user (that's Step 3)
- Pass `error=` as a template variable, not via `flash()` — the template already expects `{{ error }}`
- Re-render the form with the submitted `name` and `email` pre-filled on error (add `value=` attributes to inputs using `{{ request.form.get('field') or '' }}`)

## Definition of done
- [ ] `GET /register` still renders the form correctly
- [ ] Submitting a blank form shows "All fields are required"
- [ ] Submitting a password shorter than 8 characters shows "Password must be at least 8 characters"
- [ ] Registering with an email already in the database shows "An account with that email already exists"
- [ ] Registering with valid unique data inserts a new row in `users` with a hashed password (not plaintext)
- [ ] After successful registration, the browser redirects to `/login`
- [ ] The `name` and `email` fields retain their values when the form re-renders on error
- [ ] App starts without errors after adding `secret_key`
