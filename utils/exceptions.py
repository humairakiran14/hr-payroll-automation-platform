class HRSystemError(Exception):
    """Base exception for all HR system errors"""
    pass

class InvalidAttendanceError(HRSystemError):
    """Raised when attendance status is invalid"""
    pass

class InvalidSalaryError(HRSystemError):
    """Raised when salary value is invalid (negative or zero)"""
    pass

class EmployeeNotFoundError(HRSystemError):
    """Raised when an employee ID doesn't exist in the system"""
    pass

class DuplicateUsernameError(HRSystemError):
    """Raised when a username already exists during signup"""
    pass