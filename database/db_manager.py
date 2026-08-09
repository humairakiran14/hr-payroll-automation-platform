import sqlite3
DB_NAME = "hr_payroll.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            designation TEXT NOT NULL,
            basic_salary REAL NOT NULL
        )
    ''')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (emp_id) REFERENCES employees (emp_id)
        )
    """)



    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            emp_id INTEGER,
            FOREIGN KEY (emp_id) REFERENCES employees (emp_id)
            )

    """)
    conn.commit()
    conn.close()

def add_employee(name,department,designation,basic_salary):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
        INSERT INTO Employees (name, department, designation, basic_salary)
        VALUES (?,?,?,?)
    """,(name,department,designation,basic_salary))
    conn.commit()
    new_emp_id = cursor.lastrowid
    conn.close()
    return new_emp_id


def get_all_employees():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Employees")
    employees=cursor.fetchall()
    conn.close()
    return employees


def add_attendance(emp_id,date,status):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
        INSERT INTO Attendance (emp_id, date, status)
        VALUES (?,?,?)
    """,(emp_id,date,status))
    conn.commit()
    conn.close()

def get_attendance():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Attendance")
    attendance=cursor.fetchall()
    conn.close()
    return attendance


def add_user(username,hashed_password,role,emp_id=None):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
        INSERT INTO Users (username, password, role, emp_id)
        VALUES (?,?,?,?)
    """,(username,hashed_password,role,emp_id))
    conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, role, emp_id FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_attendance_by_emp(emp_id): #attendance records for a specific employee
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance WHERE emp_id = ?", (emp_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_present_days(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE emp_id = ? AND status = 'Present'
    """, (emp_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_employee_by_id(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
    row = cursor.fetchone()
    conn.close()
    return row
