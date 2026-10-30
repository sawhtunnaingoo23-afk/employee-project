# Aurelia People — Flask + PyMySQL + MySQL

## 1. Create database and table
Start MySQL Server. In MySQL Workbench, open `schema.sql` and execute it.
It creates database `aurelia_employee_db` and table `employees`.

Command-line alternative:
```bash
mysql -u root -p < schema.sql
```

## 2. Configure database connection (Windows PowerShell)
Defaults: host `localhost`, port `3306`, user `root`, blank password.
Set your actual MySQL password if required:
```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD="your_mysql_password"
$env:DB_NAME="aurelia_employee_db"
```

## 3. Install and run
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

The Flask app also creates the database and employees table automatically if the configured MySQL user has permission to create databases.

## Routes
- `/` — dashboard
- `/add_employee` — add employee (GET/POST)
- `/view_employees` — list and search
- `/edit_employee/<id>` — update (GET/POST)
- `/delete_employee/<id>` — delete (POST)

Change the development `SECRET_KEY`, disable debug mode, and add authentication and CSRF protection before production use.
