import streamlit as st
from utils.exceptions import InvalidSalaryError
import pandas as pd
from auth.auth_manager import check_login, hash_password
from models.employee import Employee
from datetime import date
from utils.logger import log_action
from database.backup_manager import backup_database
from database.db_manager import (
    add_employee, get_all_employees, create_tables, add_attendance,
    get_attendance, add_user, get_attendance_by_emp, get_user_by_username,
    get_present_days, get_employee_by_id
)

create_tables()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

st.title("HR & Payroll Automation System")
username = st.text_input("Enter your username")
password = st.text_input("Enter your password", type="password")

if st.button("login"):
    if role := check_login(username, password):
        st.session_state.logged_in = True
        st.session_state.role = role
        st.success(f"Logged in as {role}")
    else:
        st.error("Invalid username or password. Please try again.")

if st.session_state.logged_in:
    st.write(f"You are logged in as: {st.session_state.role}")
    role = st.session_state.role

    # ---------------- ADMIN + HR: Employee Management ----------------
    if role in ["Admin", "HR"]:
        st.subheader("ADD NEW EMPLOYEE")
        new_name = st.text_input("Employee name")
        new_dept = st.text_input("Employee department")
        new_desig = st.text_input("Employee designation")
        new_salary = st.number_input("Employee basic salary", min_value=0.0)
        new_username = st.text_input("Login Username for Employee")
        new_password = st.text_input("Login Password for Employee", type="password")

        if st.button("Add Employee"):
            if new_name and new_dept and new_desig and new_salary and new_username and new_password:
                new_emp_id = add_employee(new_name, new_dept, new_desig, new_salary)
                add_user(new_username, hash_password(new_password), "Employee", new_emp_id)
                st.success(f"Employee {new_name} added successfully with login username '{new_username}'.")
                log_action(f"New employee added: {new_name}, ID: {new_emp_id}", role)
            else:
                st.error("Please fill in all fields to add a new employee.")

        st.subheader("All Employees:")
        employees = get_all_employees()

        if employees:
            df = pd.DataFrame(employees, columns=["ID", "Name", "Department", "Designation", "Basic Salary"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No employees found. Please add employees to see the list.")


        

    # ---------------- ADMIN + HR: Attendance ----------------
    if role in ["Admin", "HR"]:
        st.subheader("Mark Attendance")
        employees = get_all_employees()
        if employees:
            emp_options = {f"{emp[0]} - {emp[1]}": emp[0] for emp in employees}
            selected_emp = st.selectbox("Select Employee", list(emp_options.keys()))
            attendance_date = st.date_input("Date", value=date.today())
            status = st.selectbox("Status", ["Present", "Absent", "Leave"])

            if st.button("Mark Attendance"):
                emp_id = emp_options[selected_emp]
                add_attendance(emp_id, str(attendance_date), status)
                st.success(f"Attendance marked: {selected_emp} - {status} on {attendance_date}")
                log_action(f"Attendance marked for Employee ID: {emp_id}, Date: {attendance_date}, Status: {status}", role)
        else:
            st.info("Add employees first before marking attendance.")

        st.subheader("All Attendance Records")
        attendance_records = get_attendance()

        if attendance_records:
            att_df = pd.DataFrame(attendance_records, columns=["ID", "Employee ID", "Date", "Status"])
            st.dataframe(att_df, use_container_width=True)
        else:
            st.info("No attendance records found.")

       # ---------------- ADMIN: Payroll and Backups ----------------
        if role == "Admin":
            st.subheader("Payroll")
            employees = get_all_employees()

            if employees:
                payroll_emp_options = {f"{emp[0]} - {emp[1]}": emp[0] for emp in employees}
                selected_payroll_emp = st.selectbox("Select Employee for Payroll", list(payroll_emp_options.keys()), key="payroll_select")

                if st.button("Calculate Salary"):
                  try:
                    emp_id = payroll_emp_options[selected_payroll_emp]
                    emp_data = get_employee_by_id(emp_id)
                    basic_salary = emp_data[4]
                    if basic_salary <= 0:
                      raise InvalidSalaryError("Employee salary must be greater than zero.")
                
                
                    present_days = get_present_days(emp_id)

                    per_day_salary = basic_salary / 30
                    final_salary = per_day_salary * present_days

                    st.success(f"Present Days: {present_days}")
                    st.success(f"Final Salary: {round(final_salary, 2)}")
                    log_action(f"Payroll calculated for Employee ID: {emp_id}, Present Days: {present_days}, Final Salary: {round(final_salary, 2)}", role)
                  except InvalidSalaryError as e:
                      st.error(f"Error: {str(e)}")
                else:
                    st.info("Add employees first to calculate payroll.")

            st.subheader("Database Backup")
            if st.button("Backup Database Now"):
                path = backup_database()
                st.success(f"Backup created: {path}")
                log_action(f"Database backup created", username)

                
    # ---------------- EMPLOYEE: My Attendance ----------------
    if role == "Employee":
        st.subheader("My Attendance")

        user_info = get_user_by_username(username)
        emp_id = user_info[3]

        my_attendance = get_attendance_by_emp(emp_id)

        if my_attendance:
            my_att_df = pd.DataFrame(my_attendance, columns=["ID", "Employee ID", "Date", "Status"])
            st.dataframe(my_att_df, use_container_width=True)
        else:
            st.info("No attendance records found for you yet.")