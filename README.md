# Student Management System

A small web application built with **Python, Flask, SQLite, and RapidFuzz**. It is packaged for editing and running in Google Antigravity IDE or another Python editor.

## Features

- Add, list, edit, and delete student records
- Unique enrollment numbers
- Input validation for age and marks
- Approximate/fuzzy search by student name or enrollment number
- Dashboard with total students, average age, average marks, and course-wise counts
- SQLite database created automatically on startup
- Responsive HTML/CSS interface

## Requirements

- Python 3.9 or newer
- Internet access once to install Python packages

## Run on Windows (PowerShell or Antigravity terminal)

1. Extract the ZIP and open the `StudentManagementSystem` folder in Antigravity.
2. Open the integrated terminal in that folder.
3. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If `py` is unavailable, use `python` instead. If PowerShell blocks activation, run `.venv\Scripts\python.exe -m pip install -r requirements.txt` and use `.venv\Scripts\python.exe app.py`.

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the application:

   ```powershell
   python app.py
   ```

6. Open **http://127.0.0.1:5000/** in your browser.

You can also double-click `run_windows.bat` after Python is installed; it creates the virtual environment if needed, installs requirements, and starts the app.

## Database and configuration

- `students.db` is created in this project folder automatically.
- To use another database path, set `STUDENT_DATABASE` before starting the app.
- Set `FLASK_SECRET_KEY` to a long random secret for any shared environment. The built-in fallback is for local development only.
- `FLASK_DEBUG=1` enables Flask debug mode. Keep it disabled outside local development.
- `PORT` can change the local port; default is `5000`.

## Antigravity agent instructions

See `GEMINI.md` and `.agent/rules/project.md` for project-specific guidance. Start by asking the agent to inspect the existing code and make incremental changes; do not replace the app wholesale unless requested.

Suggested first prompt:

> Inspect this Student Management System repository. Explain its architecture and run checks before changing anything. Identify bugs or missing features, then propose a small implementation plan. Preserve Flask, SQLite, RapidFuzz, and the existing routes unless a change is justified. Do not delete or reset `students.db`.

## Project structure

```text
StudentManagementSystem/
├── app.py
├── requirements.txt
├── run_windows.bat
├── GEMINI.md
├── .agent/rules/project.md
├── templates/
│   ├── index.html
│   ├── edit.html
│   └── analysis.html
└── static/style.css
```

## Limitations / before deployment

This is a local learning project, not a production-ready student information system. Before exposing it to a network, add authentication/authorization, CSRF protection, secure secret configuration, database backups, logging, and production hosting. Do not use Flask's development server in production.
