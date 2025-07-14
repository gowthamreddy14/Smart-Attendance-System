import sqlite3
import csv
from datetime import datetime

# ✅ Connect to your database
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# ✅ Define your month — change as needed!
month = '07' # Example: July
year = '2025'

# ✅ Get all unique working days in this month
cursor.execute('''
    SELECT DISTINCT date FROM attendance
    WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
''', (month, year))
working_days = cursor.fetchall()
total_working_days = len(working_days)

print(f"📅 Total working days in {month}-{year}: {total_working_days}")

# ✅ Get all students
cursor.execute('SELECT student_id, name FROM students')
students = cursor.fetchall()

# ✅ Prepare result list
result = []

for student_id, name in students:
    cursor.execute('''
        SELECT COUNT(*) FROM attendance
        WHERE student_id = ? AND status = 'Present'
        AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
    ''', (student_id, month, year))
    present_days = cursor.fetchone()[0]

    percentage = (present_days / total_working_days * 100) if total_working_days > 0 else 0

    result.append([student_id, name, present_days, total_working_days, round(percentage, 2)])

# ✅ Close DB
conn.close()

# ✅ Write to CSV
with open('monthly_attendance.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Student ID', 'Name', 'Days Present', 'Total Working Days', 'Attendance %'])
    writer.writerows(result)

print("✅ Monthly attendance exported to monthly_attendance.csv")
