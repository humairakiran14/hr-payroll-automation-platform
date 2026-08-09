# HR & Payroll Automation Platform

Enterprise-level HR and Payroll management system built as a Week 04 capstone project for Aptura Tech Solutions' Python Development Internship (Batch 02).

## Objective

A production-style solution demonstrating authentication, documentation, testing, scalability considerations, security, error handling, and a deployment plan — built with role-based access for Admin, HR, and Employee users.

## Tech Stack

- **Language:** Python 3.13
- **Framework:** Streamlit (web-based UI)
- **Database:** SQLite
- **Security:** SHA-256 password hashing

## Features

- **Authentication & RBAC** — Role-based login (Admin / HR / Employee), each with different access levels
- **Employee Management** — Add and view employee records (Admin/HR)
- **Attendance Management** — Mark and view attendance (Admin/HR); Employees can view their own attendance
- **Payroll** — Automatic salary calculation based on present days (Admin only)
- **Database Backup** — One-click backup with timestamped files (Admin only)
- **Logging** — All key actions logged with timestamp and user (`logs/app.log`)
- **Custom Exceptions** — Domain-specific error handling (`utils/exceptions.py`)

## Project Structure
hr_payroll_system/
├── app.py # Main Streamlit entry point
├── config.py # App configuration
├── create_admin.py # One-time script to seed Admin/HR users
├── auth/ # Authentication logic
├── database/ # Database connection, CRUD, backup
├── models/ # Data models (Employee)
├── utils/ # Logging, custom exceptions
├── logs/ # Auto-generated log files
├── backups/ # Auto-generated database backups

## Setup Instructions

1. Install dependencies: pip install streamlit
2. Create initial Admin/HR users: py create_admin.py
3. Run the app: py -m streamlit run app.py

## Default Credentials (for testing)

| Role  | Username | Password |
|-------|----------|----------|
| Admin | Admin    | admin123 |
| HR    | HR1      | hr123    |

## Author

Humaira — Python Development Intern, Aptura Tech Solutions (Batch 02)
