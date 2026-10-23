
import os
import time
from flask import Flask, request, redirect, render_template_string
import psycopg

app = Flask(__name__)

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://labuser:labpass123@localhost:5432/labdb"
)

def get_connection():
    return psycopg.connect(DATABASE_URL)

def initialize_database():
    for attempt in range(15):
        try:
            with get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(150) NOT NULL
                    )
                """)
            print("Database is ready.")
            return
        except psycopg.OperationalError:
            print("Waiting for PostgreSQL...")
            time.sleep(2)

    raise RuntimeError("Could not connect to PostgreSQL.")

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Student Records Management</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 750px;
            margin: 40px auto;
            padding: 20px;
            background: #f3f6fb;
            color: #222;
        }
        h1 { color: #234a80; }
        form, .records {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        input, button {
            padding: 10px;
            margin: 6px 0;
            width: 100%;
            box-sizing: border-box;
        }
        button {
            background: #234a80;
            color: white;
            border: 0;
            cursor: pointer;
        }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border-bottom: 1px solid #ddd; }
        th { text-align: left; }
    </style>
</head>
<body>
    <h1>Student Records Management System</h1>
    <p>Add a student and view records saved in PostgreSQL.</p>

    <form method="POST" action="/students">
        <label for="name">Student Name</label>
        <input id="name" name="name" required maxlength="100"
               placeholder="Enter student name">

        <label for="email">Student Email</label>
        <input id="email" name="email" type="email" required maxlength="150"
               placeholder="Enter student email">

        <button type="submit" id="add-student">Add Student</button>
    </form>

    <section class="records">
        <h2>Saved Students</h2>
        <table>
            <thead>
                <tr><th>ID</th><th>Name</th><th>Email</th></tr>
            </thead>
            <tbody>
                {% for student in students %}
                <tr>
                    <td>{{ student[0] }}</td>
                    <td>{{ student[1] }}</td>
                    <td>{{ student[2] }}</td>
                </tr>
                {% else %}
                <tr><td colspan="3">No students added yet.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </section>
</body>
</html>
"""

@app.route("/")
def home():
    with get_connection() as conn:
        students = conn.execute(
            "SELECT id, name, email FROM students ORDER BY id"
        ).fetchall()

    return render_template_string(PAGE, students=students)

@app.route("/students", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()

    if not name or not email:
        return "Name and email are required.", 400

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO students (name, email) VALUES (%s, %s)",
            (name, email)
        )

    return redirect("/")

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=8000)
