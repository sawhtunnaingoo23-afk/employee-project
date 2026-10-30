from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/student-form")
def student_form():
    return render_template("student_form.html")

@app.route("/student-info", methods=["POST"])
def student_info():
    name = request.form.get("student_name", "").strip()
    student_id = request.form.get("student_id", "").strip()
    email = request.form.get("email", "").strip()

    if not name or not student_id or not email:
        return render_template("student_form.html",
                               error="Please fill in all fields."), 400

    return render_template("student_result.html",
                           name=name, student_id=student_id, email=email)

@app.route("/grade-calculator")
def grade_calculator_page():
    return render_template("grade_calculator.html")

@app.route("/grade", methods=["POST"])
def calculate_grade():
    name = request.form.get("grade_student_name", "").strip()
    marks_text = request.form.get("marks", "").strip()

    if not name or not marks_text:
        return render_template("grade_calculator.html",
                               error="Please enter the student name and marks."), 400
    try:
        marks = float(marks_text)
    except ValueError:
        return render_template("grade_calculator.html",
                               error="Marks must be a number between 0 and 100."), 400

    if not 0 <= marks <= 100:
        return render_template("grade_calculator.html",
                               error="Marks must be between 0 and 100."), 400

    if marks >= 80:
        grade = "A"
    elif marks >= 60:
        grade = "B"
    elif marks >= 40:
        grade = "C"
    else:
        grade = "Fail"

    return render_template("grade_result.html", name=name, marks=marks, grade=grade)

if __name__ == "__main__":
    app.run(debug=True)
