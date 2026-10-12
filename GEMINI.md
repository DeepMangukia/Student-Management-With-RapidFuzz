# Instructions for AI coding agents

## Project goal
Maintain and improve a student CRUD web app built with Python + Flask, SQLite, Jinja templates, plain CSS, and RapidFuzz.

## Rules
- Inspect existing files and explain a short plan before making broad changes.
- Preserve current features: add/list/edit/delete students, fuzzy search, and analysis dashboard.
- Do not migrate frameworks or add large dependencies without a clear reason and user approval.
- Never delete, overwrite, or reset `students.db`; preserve student data during schema changes.
- Use parameterized SQL queries. Do not build SQL by concatenating user input.
- Validate form data on the server, not only in HTML.
- Keep templates accessible and responsive; retain Jinja autoescaping.
- Keep secrets out of source control. The local development secret is not suitable for deployment.
- Avoid enabling Flask debug mode by default.
- Add or update tests for behavior changes and run available tests before reporting completion.
- Report changed files, commands run, test results, and any known limitations honestly.
