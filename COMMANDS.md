# Commands Run — Expense Tracker Practice

## 1. `python3 -m venv venv`
Creates a virtual environment — a private, isolated folder with its own copy of Python just for this project. The `-m venv` part tells Python to run its built-in virtual environment tool, and the second `venv` is the name of the folder it creates. This keeps project dependencies separate from your system Python.

## 2. `source venv/bin/activate`
Activates the virtual environment by telling your terminal to use the Python and tools inside the `venv/` folder instead of the system ones. This only affects your current terminal session — closing the terminal deactivates it.

## 3. `pip install -r requirements.txt`
`pip` is Python's package manager. The `-r` flag tells it to read from a file and install everything listed in it. This downloaded and installed all the libraries this project depends on (Flask, Werkzeug, pytest, pytest-flask) into the virtual environment.

## 4. `python3 app.py`
Runs the app by executing `app.py` as the entry point. Flask starts a local web server on port 5001 with debug mode on (auto-reloads when you change files). The app is accessible at `http://127.0.0.1:5001` — `127.0.0.1` means "this machine only", not the internet.

## 5. `git init`
Initializes a new Git repository in the project folder. Git is a version control system — it tracks every change you make to your code over time. This creates a hidden `.git/` folder that stores the entire history.

## 6. `git add .`
Stages all files in the project for the next commit. The `.` means "everything in the current directory." Staging is like telling Git "include these files in the next snapshot."

## 7. `git commit -m 'initial commit'`
Creates the first snapshot (commit) of the project with the message "initial commit". A commit is a saved checkpoint — you can always go back to it if something breaks later.

## 8. `git remote add origin https://github.com/11699111b-ship-it/spendlypractice.git`
Links your local repository to a remote one on GitHub. `origin` is just the conventional name for your main remote. This tells Git where to push your code when you want to back it up or share it.

## 9. `git branch -M main`
Renames the default branch from `master` to `main`. Modern convention uses `main` as the primary branch name, and GitHub expects it by default.

## 10. `git push -u origin main`
Uploads your local commits to GitHub for the first time. The `-u` flag sets `origin main` as the default, so future pushes can just be `git push` without specifying where to push.
