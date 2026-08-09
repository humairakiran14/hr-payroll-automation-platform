# Testing Report — HR & Payroll Automation Platform

**Project:** Enterprise HR & Payroll Automation Platform
**Prepared by:** Humaira — Python Development Intern, Aptura Tech Solutions (Batch 02)
**Date:** August 2026

## 1. Testing Approach

Testing was performed manually through the Streamlit UI, covering authentication, role-based access control, employee management, attendance tracking, payroll calculation, and database backup. Each feature was tested with valid inputs, invalid inputs, and edge cases where applicable.

## 2. Test Cases

| # | Module | Test Case | Input | Expected Result | Actual Result | Status |
|---|--------|-----------|-------|------------------|----------------|--------|
| 1 | Authentication | Valid Admin login | Username: Admin, Password: admin123 | Login successful, role = Admin | Login successful, role = Admin | Pass |
| 2 | Authentication | Valid HR login | Username: HR1, Password: hr123 | Login successful, role = HR | Login successful, role = HR | Pass |
| 3 | Authentication | Invalid password | Username: Admin, Password: wrongpass | Error: Invalid username or password | Error displayed correctly | Pass |
| 4 | Authentication | Non-existent username | Username: xyz123, Password: 1234 | Error: Invalid username or password | Error displayed correctly | Pass |
| 5 | Authentication | Password hashing | Any valid login | Password stored as SHA-256 hash, not plain text | Confirmed hash stored in database | Pass |
| 6 | RBAC | Employee login access | Login as Employee role | Only "My Attendance" section visible; no Add Employee, Payroll, or Backup | Confirmed — only own attendance shown | Pass |
| 7 | RBAC | HR login access | Login as HR role | Employee Management + Attendance visible; Payroll and Backup hidden | Confirmed — Payroll/Backup not shown | Pass |
| 8 | RBAC | Admin login access | Login as Admin role | Full access to all modules | Confirmed — all sections visible | Pass |
| 9 | Employee Management | Add new employee (valid data) | Name, Department, Designation, Salary, Username, Password all filled | Employee added, login credentials created, success message shown | Employee added successfully with new login | Pass |
| 10 | Employee Management | Add employee with missing fields | Leave Salary field empty | Error: Please fill in all fields | Error displayed, employee not added | Pass |
| 11 | Employee Management | View all employees | Click into Employees table | Table displays ID, Name, Department, Designation, Salary | Table rendered correctly | Pass |
| 12 | Attendance | Mark attendance (Present) | Select employee, today's date, status = Present | Record inserted, success message shown | Attendance recorded correctly | Pass |
| 13 | Attendance | Mark attendance with no employees in system | Attempt to mark attendance on empty employee list | Info message: Add employees first | Info message displayed | Pass |
| 14 | Attendance | Employee views own attendance | Login as Employee, open My Attendance | Only that employee's own records shown | Confirmed — no other employee data visible | Pass |
| 15 | Payroll | Calculate salary for employee with attendance | Select employee with 2 present days, basic salary 50000 | Final salary = (50000/30) × 2 = 3333.33 | Calculated correctly, displayed as 3333.33 | Pass |
| 16 | Payroll | Calculate salary for employee with zero present days | Select employee with no attendance marked | Final salary = 0 | Displayed 0 as expected | Pass |
| 17 | Payroll | Access restriction | Login as HR, attempt to reach Payroll section | Payroll section not visible/accessible | Confirmed — HR cannot access Payroll | Pass |
| 18 | Database Backup | Create backup as Admin | Click "Backup Database Now" | Timestamped .db file created in backups/ folder | Backup file created successfully | Pass |
| 19 | Database Backup | Access restriction | Login as HR, attempt to reach Backup section | Backup section not visible | Confirmed — HR cannot access Backup | Pass |
| 20 | Logging | Action logging | Perform employee add, attendance mark, payroll calculation, backup | Each action logged in logs/app.log with timestamp and user | All actions logged correctly | Pass |

## 3. Known Limitations

- **Salary calculation is simplified** — assumes a fixed 30-day month and does not account for leaves, overtime, tax deductions, or bonuses.
- **No password strength validation** — the system accepts any password length/complexity for new employee logins.
- **No duplicate username check at UI level** — if two employees are given the same username, the second insert will fail at the database level (UNIQUE constraint) without a friendly error message.
- **Single-admin bootstrap** — Admin/HR accounts must be seeded manually via `create_admin.py`; there is no in-app "create Admin" flow.
- **No password reset/forgot password flow** — a user who forgets their password must be reset manually by an Admin at the database level.
- **SQLite is used for development** — not designed for very high concurrent write loads; a production deployment at enterprise scale would require migration to PostgreSQL/MySQL (see Deployment Plan).
- **No pagination** — Employee and Attendance tables display all records at once; with very large datasets this could slow down page rendering.

## 4. Conclusion

All core functional test cases passed successfully. The system correctly enforces role-based access control, calculates payroll accurately based on attendance, and logs all significant actions. The known limitations listed above are primarily scalability and UX polish items appropriate for a future iteration beyond this capstone scope.
