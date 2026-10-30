import os
import re
from datetime import date

import pymysql
from pymysql.cursors import DictCursor
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-secret-key-before-deployment")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "aurelia_employee_db"),
    "charset": "utf8mb4",
    "cursorclass": DictCursor,
    "autocommit": False,
}

DEPARTMENTS = ["IT", "HR", "Finance", "Marketing", "Administration"]
GENDERS = ["Male", "Female", "Other"]

def get_db():
    if "db" not in g:
        g.db = pymysql.connect(**DB_CONFIG)
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    # Connect without selecting a database, then create it if needed.
    server = pymysql.connect(
        host=DB_CONFIG["host"], port=DB_CONFIG["port"],
        user=DB_CONFIG["user"], password=DB_CONFIG["password"],
        charset=DB_CONFIG["charset"], cursorclass=DictCursor
    )
    try:
        with server.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        server.commit()
    finally:
        server.close()

    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    employee_id VARCHAR(30) PRIMARY KEY,
                    full_name VARCHAR(120) NOT NULL,
                    email VARCHAR(254) NOT NULL,
                    phone VARCHAR(25) NOT NULL,
                    gender ENUM('Male', 'Female', 'Other') NOT NULL,
                    department ENUM('IT', 'HR', 'Finance', 'Marketing', 'Administration') NOT NULL,
                    position VARCHAR(100) NOT NULL,
                    salary DECIMAL(12, 2) NOT NULL,
                    joining_date DATE NOT NULL,
                    CONSTRAINT chk_positive_salary CHECK (salary > 0)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
        db.commit()
    except Exception:
        db.rollback()
        raise

def validate_employee(form, editing=False, current_id=None):
    data = {key: form.get(key, "").strip() for key in (
        "employee_id", "full_name", "email", "phone", "gender",
        "department", "position", "salary", "joining_date"
    )}
    errors = []
    if any(not value for value in data.values()):
        errors.append("Please complete every required field.")
    if data["email"] and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", data["email"]):
        errors.append("Enter a valid email address.")
    if data["phone"] and not re.fullmatch(r"[+\d\s()\-]{7,20}", data["phone"]):
        errors.append("Phone number must be 7–20 characters and contain only digits, spaces, +, brackets or hyphens.")
    try:
        salary = float(data["salary"])
        if salary <= 0:
            raise ValueError
        data["salary"] = salary
    except (ValueError, TypeError):
        errors.append("Salary must be a positive numeric value.")
    if data["gender"] and data["gender"] not in GENDERS:
        errors.append("Select a valid gender.")
    if data["department"] and data["department"] not in DEPARTMENTS:
        errors.append("Select a valid department.")
    if data["joining_date"]:
        try:
            date.fromisoformat(data["joining_date"])
        except ValueError:
            errors.append("Enter a valid joining date.")
    if data["employee_id"]:
        with get_db().cursor() as cursor:
            cursor.execute(
                "SELECT employee_id FROM employees WHERE employee_id = %s",
                (data["employee_id"],)
            )
            existing = cursor.fetchone()
        if existing and not (editing and data["employee_id"] == current_id):
            errors.append("That Employee ID already exists. Please use a unique ID.")
    return data, errors

@app.route("/")
def home():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM employees")
        total = cursor.fetchone()["total"]
        cursor.execute("SELECT COUNT(DISTINCT department) AS departments FROM employees")
        departments = cursor.fetchone()["departments"]
        cursor.execute("SELECT COALESCE(SUM(salary), 0) AS payroll FROM employees")
        payroll = cursor.fetchone()["payroll"]
        cursor.execute("SELECT * FROM employees ORDER BY joining_date DESC LIMIT 5")
        recent = cursor.fetchall()
    return render_template("index.html",
        stats={"total": total, "departments": departments, "payroll": payroll},
        recent=recent)

@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        data, errors = validate_employee(request.form)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("employee_form.html", employee=data, mode="add",
                departments=DEPARTMENTS, genders=GENDERS)
        db = get_db()
        try:
            with db.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO employees
                    (employee_id, full_name, email, phone, gender, department, position, salary, joining_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, tuple(data[k] for k in (
                    "employee_id", "full_name", "email", "phone", "gender",
                    "department", "position", "salary", "joining_date"
                )))
            db.commit()
        except pymysql.err.IntegrityError:
            db.rollback()
            flash("That Employee ID already exists. Please use a unique ID.", "error")
            return render_template("employee_form.html", employee=data, mode="add",
                departments=DEPARTMENTS, genders=GENDERS)
        flash(f'{data["full_name"]} has been added successfully.', "success")
        return redirect(url_for("view_employees"))
    return render_template("employee_form.html", employee={}, mode="add",
        departments=DEPARTMENTS, genders=GENDERS)

@app.route("/view_employees")
def view_employees():
    q = request.args.get("q", "").strip()
    with get_db().cursor() as cursor:
        if q:
            cursor.execute("""
                SELECT * FROM employees
                WHERE employee_id LIKE %s OR full_name LIKE %s OR department LIKE %s OR position LIKE %s
                ORDER BY full_name
            """, tuple([f"%{q}%"] * 4))
        else:
            cursor.execute("SELECT * FROM employees ORDER BY full_name")
        employees = cursor.fetchall()
    return render_template("employees.html", employees=employees, q=q)

@app.route("/edit_employee/<id>", methods=["GET", "POST"])
def edit_employee(id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM employees WHERE employee_id = %s", (id,))
        employee = cursor.fetchone()
    if employee is None:
        flash("Employee record could not be found.", "error")
        return redirect(url_for("view_employees"))
    if request.method == "POST":
        data, errors = validate_employee(request.form, editing=True, current_id=id)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("employee_form.html", employee=data, mode="edit",
                departments=DEPARTMENTS, genders=GENDERS, original_id=id)
        try:
            with db.cursor() as cursor:
                cursor.execute("""
                    UPDATE employees SET employee_id=%s, full_name=%s, email=%s, phone=%s,
                    gender=%s, department=%s, position=%s, salary=%s, joining_date=%s
                    WHERE employee_id=%s
                """, tuple(data[k] for k in (
                    "employee_id", "full_name", "email", "phone", "gender",
                    "department", "position", "salary", "joining_date"
                )) + (id,))
            db.commit()
        except pymysql.err.IntegrityError:
            db.rollback()
            flash("That Employee ID already exists. Please use a unique ID.", "error")
            return render_template("employee_form.html", employee=data, mode="edit",
                departments=DEPARTMENTS, genders=GENDERS, original_id=id)
        flash(f'{data["full_name"]}’s record has been updated.', "success")
        return redirect(url_for("view_employees"))
    return render_template("employee_form.html", employee=employee, mode="edit",
        departments=DEPARTMENTS, genders=GENDERS, original_id=id)

@app.route("/delete_employee/<id>", methods=["POST"])
def delete_employee(id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT full_name FROM employees WHERE employee_id = %s", (id,))
        employee = cursor.fetchone()
        if employee:
            cursor.execute("DELETE FROM employees WHERE employee_id = %s", (id,))
    db.commit()
    if employee:
        flash(f'{employee["full_name"]} has been removed.', "success")
    else:
        flash("Employee record could not be found.", "error")
    return redirect(url_for("view_employees"))

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
