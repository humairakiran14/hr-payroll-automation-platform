import hashlib
from database.db_manager import get_user_by_username

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username,password):
    user=get_user_by_username(username)
    if user:
        stored_username,stored_password,role,emp_id= user
        hashed_input=hash_password(password)
        if stored_password == hashed_input:
            return role
    return None

