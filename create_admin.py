from auth.auth_manager import hash_password
from database.db_manager import add_user,create_tables

create_tables()
#admin
add_user("Admin",hash_password("admin123"),"Admin",None)

#HR
add_user("HR1",hash_password("hr123"),"HR",None)
add_user("HR2",hash_password("hr456"),"HR",None)

print("Admin and HR users created successfully.")
