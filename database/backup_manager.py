import shutil
import os
from datetime import datetime

def backup_database():
    os.makedirs("backups", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backups/hr_payroll_backup_{timestamp}.db"
    shutil.copy("hr_payroll.db", backup_path)
    return backup_path