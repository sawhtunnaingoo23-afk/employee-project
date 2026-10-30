# Project Report: Aurelia People — Employee Management System

## 1. Introduction

Aurelia People is a web-based Employee Management System developed with the Python Flask framework, HTML templates, CSS, and an MySQL database. It allows an administrator to register employees, view employee information, update employee records, and delete records.

The interface uses a premium navy, warm gold, ivory, and white visual identity. It is responsive and includes a dashboard, employee directory, and employee form.

## 2. System architecture

The application follows a simple Flask / template / database architecture:

- **Presentation layer:** Jinja2 HTML templates in `templates/` display the dashboard, registration/edit form, and employee directory.
- **Styling layer:** `static/css/style.css` provides the visual design and responsive layouts.
- **Application layer:** `app.py` defines routes, processes GET and POST requests, validates form input, and performs database operations.
- **Data layer:** MySQL stores employee records in the `employees` table. The database is created automatically when the application starts.

## 3. Database design

The `employees` table contains the following attributes:

| Attribute | MySQL type | Purpose |
|---|---|---|
| employee_id | TEXT PRIMARY KEY | Unique employee identifier |
| full_name | TEXT | Employee full name |
| email | TEXT | Email address |
| phone | TEXT | Phone number |
| gender | TEXT | Male, Female, or Other |
| department | TEXT | IT, HR, Finance, Marketing, or Administration |
| position | TEXT | Job position |
| salary | REAL | Positive salary amount |
| joining_date | TEXT | Date of joining in ISO format |

Parameterized SQL statements are used for insert, select, update, and delete operations.

## 4. Flask routing

- `/` displays the home dashboard and summary statistics.
- `/add_employee` displays the registration form with GET and inserts a new employee with POST.
- `/view_employees` retrieves all employee records and displays them in an HTML table. It also supports a simple search query.
- `/edit_employee/<id>` retrieves one employee with GET and updates the record with POST.
- `/delete_employee/<id>` deletes the selected employee using POST. A browser confirmation is shown before submission.

## 5. CRUD operations

- **Create:** The administrator enters the nine requested fields and submits the form.
- **Read:** The directory displays stored employee records in a table.
- **Update:** The edit page loads an employee's current values and saves changes.
- **Delete:** The delete action removes the selected record after confirmation.

Flash messages report successful operations and validation or lookup errors.

## 6. Input validation

The application checks that all required fields are present, the email has a valid basic format, salary is numeric and greater than zero, the employee ID is unique, and the phone number contains accepted characters and has an acceptable length. Gender and department values are also checked against the assignment's allowed options.

## 7. Testing plan

Run the following tests in the browser:

| Test | Steps | Expected result |
|---|---|---|
| Valid registration | Add an employee with all valid fields | Record is saved and success message appears |
| Missing information | Submit with one or more required fields empty | Browser validation and/or server validation prevents saving |
| Duplicate ID | Register an existing Employee ID again | Error message; duplicate is not saved |
| Update record | Edit an employee and save | Updated values appear in the directory |
| Delete record | Select delete and confirm | Record is removed and success message appears |
| View records | Open Employees | All stored records appear in the table |

## 8. Conclusion

The project fulfils the five practical tasks by providing a responsive employee registration form, the required Flask routes, MySQL database integration, complete CRUD functionality, and input validation with a testing plan. The source code is organised into an application file, templates, and a separate CSS file.


## MySQL and PyMySQL
The Flask application uses PyMySQL to connect to the `aurelia_employee_db` database and its `employees` table. Run `schema.sql` in MySQL Workbench to create the schema. Connection settings are configurable using DB_HOST, DB_PORT, DB_USER, DB_PASSWORD and DB_NAME environment variables.
