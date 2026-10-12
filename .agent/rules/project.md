# Student Management System project rule

- Stack: Python 3, Flask, SQLite, RapidFuzz, Jinja2, HTML/CSS.
- Keep the project beginner-friendly and runnable on Windows.
- Prefer small, reversible changes over rewrites.
- Preserve existing routes and database records unless the user explicitly requests otherwise.
- Validate enrollment, name, course, age, and marks on the server.
- Use SQL parameters for every value derived from user input.
- Never commit `.env`, `.venv/`, `__pycache__/`, or the local SQLite database.
- For a feature change, verify relevant routes manually or with tests and summarize the result.
