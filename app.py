from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3
from pathlib import Path
from rapidfuzz import fuzz, process

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")
BASE_DIR = Path(__file__).resolve().parent
DATABASE = os.environ.get("STUDENT_DATABASE", str(BASE_DIR / "students.db"))


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enrollment TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                course TEXT NOT NULL,
                marks REAL NOT NULL
            )
        """)


@app.route("/")
def index():
    search = request.args.get("search", "").strip()

    with get_db() as conn:
        students = conn.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()

    if search:
        # Each search option maps back to the corresponding student ID.
        choices = {}
        for student in students:
            choices[f"name:{student['id']}"] = student["name"]
            choices[f"enrollment:{student['id']}"] = student["enrollment"]

        matches = process.extract(
            search, choices, scorer=fuzz.WRatio,
            limit=None, score_cutoff=50
        )
        matched_ids = {int(key.split(":")[1]) for _, _, key in matches}
        students = [s for s in students if s["id"] in matched_ids]

    return render_template("index.html", students=students, search=search)


@app.route("/add", methods=["POST"])
def add_student():
    enrollment = request.form.get("enrollment", "").strip()
    name = request.form.get("name", "").strip()
    course = request.form.get("course", "").strip()

    try:
        age = int(request.form.get("age", ""))
        marks = float(request.form.get("marks", ""))

        if not enrollment or not name or not course:
            raise ValueError("All fields are required.")
        if age < 1:
            raise ValueError("Age must be at least 1.")
        if not 0 <= marks <= 100:
            raise ValueError("Marks must be between 0 and 100.")

        with get_db() as conn:
            conn.execute(
                """INSERT INTO students (enrollment, name, age, course, marks)
                   VALUES (?, ?, ?, ?, ?)""",
                (enrollment, name, age, course, marks)
            )
        flash("Student added successfully!", "success")

    except sqlite3.IntegrityError:
        flash("Enrollment number already exists.", "error")
    except ValueError as error:
        flash(str(error) or "Please enter valid details.", "error")

    return redirect(url_for("index"))


@app.route("/update/<int:student_id>", methods=["GET", "POST"])
def update_student(student_id):
    if request.method == "POST":
        enrollment = request.form.get("enrollment", "").strip()
        name = request.form.get("name", "").strip()
        course = request.form.get("course", "").strip()

        try:
            age = int(request.form.get("age", ""))
            marks = float(request.form.get("marks", ""))

            if not enrollment or not name or not course:
                raise ValueError("All fields are required.")
            if age < 1:
                raise ValueError("Age must be at least 1.")
            if not 0 <= marks <= 100:
                raise ValueError("Marks must be between 0 and 100.")

            with get_db() as conn:
                conn.execute(
                    """UPDATE students
                       SET enrollment=?, name=?, age=?, course=?, marks=?
                       WHERE id=?""",
                    (enrollment, name, age, course, marks, student_id)
                )
            flash("Student updated successfully!", "success")
            return redirect(url_for("index"))

        except sqlite3.IntegrityError:
            flash("Enrollment number already exists.", "error")
        except ValueError as error:
            flash(str(error) or "Please enter valid details.", "error")

        return redirect(url_for("update_student", student_id=student_id))

    with get_db() as conn:
        student = conn.execute(
            "SELECT * FROM students WHERE id=?", (student_id,)
        ).fetchone()

    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("index"))

    return render_template("edit.html", student=student)


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_db() as conn:
        conn.execute("DELETE FROM students WHERE id=?", (student_id,))
    flash("Student deleted successfully!", "success")
    return redirect(url_for("index"))


@app.route("/analysis")
def analysis():
    with get_db() as conn:
        summary = conn.execute("""
            SELECT COUNT(*) AS total,
                   ROUND(AVG(age), 2) AS average_age,
                   ROUND(AVG(marks), 2) AS average_marks
            FROM students
        """).fetchone()
        courses = conn.execute("""
            SELECT course, COUNT(*) AS total
            FROM students GROUP BY course ORDER BY total DESC
        """).fetchall()

    return render_template("analysis.html", summary=summary, courses=courses)


# Initialize the database when the app is imported or started.
create_table()

if __name__ == "__main__":
    debug_enabled = os.environ.get("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=debug_enabled)
