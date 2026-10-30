from flask import Flask, flash, redirect, render_template, request, url_for
import pymysql

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)
app.secret_key = "change-this-for-your-project"

# MySQL Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'students_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    # Note: Ensure the database 'students_db' is already created in MySQL before running this
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL
                )
            """)
        conn.commit()
    finally:
        conn.close()

# --- ROUTES ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/students")
def students():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM students ORDER BY id DESC")
            records = cursor.fetchall()
    finally:
        conn.close()
    return render_template("students.html", students=records)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        
        if not name or not email:
            flash("Please enter both name and email.")
            return redirect(url_for("add_student"))
            
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO students (name, email) VALUES (%s, %s)", (name, email)
                )
            conn.commit()
        finally:
            conn.close()
        
        flash("Student added successfully!")
        return redirect(url_for("students"))
        
    return render_template("add_student.html")

# --- EDIT STUDENT ROUTE ---

@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM students WHERE id = %s",
                (student_id,)
            )
            student = cursor.fetchone()

            if student is None:
                flash("Student not found.")
                return redirect(url_for("students"))

            if request.method == "POST":
                name = request.form.get("name", "").strip()
                email = request.form.get("email", "").strip()

                if not name or not email:
                    flash("Name and email are required.")
                    return redirect(
                        url_for("edit_student", student_id=student_id)
                    )

                cursor.execute(
                    """
                    UPDATE students
                    SET name = %s, email = %s
                    WHERE id = %s
                    """,
                    (name, email, student_id)
                )
                conn.commit()
                flash("Student updated successfully!")
                return redirect(url_for("students"))

        return render_template("edit_student.html", student=student)
    finally:
        conn.close()

# --- DELETE STUDENT ROUTE ---

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM students WHERE id = %s",
                (student_id,)
            )
        conn.commit()
        flash("Student deleted successfully!")
    except Exception:
        conn.rollback()
        flash("Unable to delete student.")
    finally:
        conn.close()

    return redirect(url_for("students"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)