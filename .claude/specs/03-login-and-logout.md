# Spec: Login and Logout

## Overview
Wire up the `/login` route to accept POST submissions, validate credentials against the database, and store the authenticated user's id and name in the Flask session. Implement `/logout` to clear the session and redirect to the landing page. After this step, the app has a working auth cycle: register → login → logout. Session state should be reflected in the nav (show "Logout" when logged in, "Login" when not).

## Depends on
- Step 1 (Database Setup) — `get_db()`, `users` table with `password_hash` must exist.
- Step 2 (Registration) — users must be insertable before login can work.

## Routes
- `GET /login` — renders the login form — public (already exists, keep as-is)
- `POST /login` — validates credentials, sets session on success, re-renders form on failure — public
- `GET /logout` — clears session, redirects to `/` — public (stub exists, implement it)

## Database changes
No database changes. The `users` table already has `id`, `name`, `email`, `password_hash`.

## Templates
- **Modify:** `templates/login.html` — add `method="POST"` to the `<form>`, add `{% if error %}` error block, pre-fill `email` field value on error using `{{ request.form.get('email') or '' }}`
- **Modify:** `templates/base.html` — update nav to show "Logout" link when `session.user_id` is set, and "Login" / "Register" links when it is not

## Files to change
- `app.py` — convert `/login` to accept GET+POST; implement `/logout`; add `check_password_hash` to the werkzeug import

## Files to create
None.

## New dependencies
No new pip packages. `check_password_hash` is already in `werkzeug.security` (same package as `generate_password_hash`).

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` via `get_db()` only
- Parameterised queries only — never string-format SQL
- Verify passwords with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Session keys: `session["user_id"]` (int) and `session["user_name"]` (str) — set both on login, clear both on logout via `session.clear()`
- Use a single generic error message for login failure: `"Invalid email or password"` — never reveal whether the email exists
- Look up the user by email only; then verify the password hash in Python, not SQL
- After successful login, redirect to `/` (landing) — a dashboard route does not exist yet
- After logout, redirect to `/` (landing)
- `GET /login` when already logged in should still render the form (no redirect guard needed at this step)

## Definition of done
- [ ] `GET /login` renders the login form
- [ ] Submitting blank fields shows "Invalid email or password"
- [ ] Submitting a valid email with a wrong password shows "Invalid email or password"
- [ ] Submitting a non-existent email shows "Invalid email or password"
- [ ] Submitting valid credentials sets the session and redirects to `/`
- [ ] After login, `session["user_id"]` and `session["user_name"]` are set
- [ ] The nav in `base.html` shows "Logout" when logged in and "Login"/"Register" when not
- [ ] Visiting `/logout` clears the session and redirects to `/`
- [ ] After logout, the nav reverts to showing "Login"/"Register"
- [ ] The `email` field retains its value when the login form re-renders on error
