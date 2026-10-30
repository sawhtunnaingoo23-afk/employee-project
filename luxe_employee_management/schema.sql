-- Aurelia People | MySQL database and table setup
CREATE DATABASE IF NOT EXISTS aurelia_employee_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE aurelia_employee_db;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_employees_full_name ON employees(full_name);
CREATE INDEX idx_employees_department ON employees(department);
